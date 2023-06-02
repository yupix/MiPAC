from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.drive import File, Folder
from mipac.types.drive import FolderPayload, IDriveFile
from mipac.utils.format import bool_to_string, remove_dict_empty
from mipac.utils.pagination import Pagination
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ('DriveActions', 'FileActions', 'FolderActions')


class ClientFileActions(AbstractAction):
    def __init__(
        self,
        file_id: str | None = None,
        folder_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ) -> None:
        self._session: HTTPClient = session
        self._client: ClientManager = client
        self._file_id = file_id
        self._folder_id = folder_id

    async def remove(self, file_id: str | None = None) -> bool:
        """
        指定したIDのファイルを削除します

        Parameters
        ----------
        file_id : str | None, default=None
            削除するファイルのID

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        file_id = file_id or self._file_id
        return bool(
            await self._session.request(
                Route('POST', '/api/drive/files/delete'), json={'fileId': file_id}, auth=True,
            )
        )

    @deprecated
    async def remove_file(self, file_id: str | None = None) -> bool:
        """
        指定したIDのファイルを削除します

        Parameters
        ----------
        file_id : str | None, default=None
            削除するファイルのID

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        file_id = file_id or self._file_id
        return bool(
            await self._session.request(
                Route('POST', '/api/drive/files/delete'), json={'fileId': file_id}, auth=True,
            )
        )


class FileActions(ClientFileActions):
    def __init__(
        self,
        file_id: str | None = None,
        folder_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ) -> None:
        super().__init__(file_id=file_id, folder_id=folder_id, session=session, client=client)

    async def show_file(self, file_id: str | None = None, url: str | None = None) -> File:
        """
        ファイルの情報を取得します。

        Parameters
        ----------
        file_id : str | None, default=None
            ファイルのID
        url : str | None, default=None
            ファイルのURL

        Returns
        -------
        File
            ファイルの情報
        """

        data = remove_dict_empty({'fileId': file_id, 'url': url})
        res: IDriveFile = await self._session.request(
            Route('POST', '/api/admin/drive/show-file'), json=data, auth=True, lower=True,
        )
        return File(res, client=self._client)

    async def get_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        file_type: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[File, None]:
        """
        ファイルを取得します

        Parameters
        ----------
        limit : int, default=10
            取得する上限
        since_id : str | None, default=None
            指定すると、そのIDを起点としてより新しいファイルを取得します
        until_id : str | None, default=None
            指定すると、そのIDを起点としてより古いファイルを取得します
        folder_id : str | None, default=None
            指定すると、そのフォルダーを起点としてファイルを取得します
        file_type : str | None, default=None
            取得したいファイルの拡張子
        """
        if limit > 100:
            raise ParameterError('limit must be less than 100')

        if get_all:
            limit = 100

        folder_id = self._folder_id or folder_id

        body = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'folderId': folder_id,
            'Type': file_type,
        }

        pagination = Pagination[IDriveFile](
            self._session, Route('POST', '/api/drive/files'), json=body
        )

        while True:
            res_drive_files = await pagination.next()

            for res_drive_file in res_drive_files:
                yield File(res_drive_file, client=self._client)

            if get_all is False or pagination.is_final:
                break

    async def upload_file(
        self,
        file: str,
        file_name: str | None = None,
        folder_id: str | None = None,
        comment: str | None = None,
        is_sensitive: bool = False,
        force: bool = False,
    ) -> File:
        """
        ファイルをアップロードします

        Parameters
        ----------
        file : str
            アップロードするファイル
        file_name : str | None, default=None
            アップロードするファイルの名前
        folder_id : str | None, default=None
            アップロードするフォルダーのID
        comment : str | None, default=None
            アップロードするファイルのコメント
        is_sensitive : bool, default=False
            アップロードするファイルがNSFWかどうか
        force : bool, default=False
            アップロードするファイルが同名のファイルを上書きするかどうか

        Returns
        -------
        File
            アップロードしたファイルの情報
        """
        file_byte = open(file, 'rb') if file else None
        folder_id = self._folder_id or folder_id

        data = {
            'file': file_byte,
            'name': file_name,
            'folderId': folder_id,
            'comment': comment,
            'isSensitive': bool_to_string(is_sensitive),
            'force': bool_to_string(force),
        }
        res: IDriveFile = await self._session.request(
            Route('POST', '/api/drive/files/create'), data=data, auth=True, lower=True,
        )
        return File(res, client=self._client)


class ClientFolderActions(AbstractAction):
    def __init__(
        self, folder_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        self._folder_id = folder_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(self, name: str, parent_id: str | None = None) -> bool:
        """
        フォルダーを作成します

        Parameters
        ----------
        name : str, default=None
            フォルダーの名前
        parent_id : str | None, default=None
            親フォルダーのID

        Returns
        -------
        bool
            作成に成功したか否か
        """
        parent_id = parent_id or self._folder_id

        data = {'name': name, 'parent_id': parent_id}
        res: bool = await self._session.request(
            Route('POST', '/api/drive/folders/create'), json=data, lower=True, auth=True,
        )
        return bool(res)

    async def delete(self, folder_id: str | None = None) -> bool:
        """
        Parameters
        ----------
        folder_id : str | None = None
            削除するノートのID

        Returns
        -------
        bool
            削除に成功したか否か
        """
        folder_id = folder_id or self._folder_id
        data = {'folderId': folder_id}
        res: bool = await self._session.request(
            Route('POST', '/api/drive/folders/delete'), json=data, lower=True, auth=True,
        )
        return bool(res)

    async def get_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        file_type: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[File, None]:
        """
        ファイルを取得します

        Parameters
        ----------
        limit : int, default=10
            取得する上限
        since_id : str | None, default=None
            指定すると、そのIDを起点としてより新しいファイルを取得します
        until_id : str | None, default=None
            指定すると、そのIDを起点としてより古いファイルを取得します
        folder_id : str | None, default=None
            指定すると、そのフォルダーを起点としてファイルを取得します
        file_type : str | None, default=None
            取得したいファイルの拡張子
        """
        if limit > 100:
            raise ParameterError('limit must be less than 100')

        if get_all:
            limit = 100

        folder_id = self._folder_id or folder_id

        body = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'folderId': folder_id,
            'Type': file_type,
        }

        pagination = Pagination[IDriveFile](
            self._session, Route('POST', '/api/drive/files'), json=body
        )

        while True:
            res_drive_files = await pagination.next()

            for res_drive_file in res_drive_files:
                yield File(res_drive_file, client=self._client)

            if get_all is False or pagination.is_final:
                break


class FolderActions(ClientFolderActions):
    def __init__(
        self, folder_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        super().__init__(folder_id=folder_id, session=session, client=client)


class DriveActions(AbstractAction):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_folders(
        self,
        limit: int = 100,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        get_all: bool=False
    ) -> AsyncGenerator[Folder, None]:
        """
        フォルダーの一覧を取得します

        Parameters
        ----------
        limit : int, default=10
            取得する上限
        since_id : str | None, default=None
            指定すると、その投稿を投稿を起点としてより新しい投稿を取得します
        until_id : str | None, default=None
            指定すると、その投稿を投稿を起点としてより古い投稿を取得します
        folder_id : str | None, default=None
            指定すると、そのフォルダーを起点としてフォルダーを取得します
        get_all : bool, default=False
            Whether to retrieve all folders or not
        """

        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if get_all:
            limit = 100

        body = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'folderId': folder_id,
        }
        
        pagination = Pagination[FolderPayload](self._session, Route('POST', '/api/drive/folders'), json=body)
        
        while True:
            res_folders = await pagination.next()
            for res_folder in res_folders:
                yield Folder(res_folder,client=self._client)
            if get_all is False or pagination.is_final:
                break
