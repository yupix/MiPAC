from __future__ import annotations

import io
import os
from typing import TYPE_CHECKING, Any, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import File
from mipac.models.note import Note
from mipac.types.drive import IDriveSort, IFile
from mipac.types.note import INote
from mipac.utils.format import bool_to_string, remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedFileActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_attached_notes(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        file_id: str,
    ) -> list[Note]:
        """Get the attached notes of a file

        Endpoint: `/api/drive/files/attached-notes`

        Parameters
        ----------
        since_id: str | None
            The id of the note to start from, defaults to None
        until_id: str | None
            The id of the note to end at, defaults to None
        limit: int
            The amount of notes to get, defaults to 10
        file_id: str | None
            The id of the file to get notes from, defaults to None

        Returns
        -------
        list[Note]
            The attached notes of the file
        """
        body = {
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "fileId": file_id,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/drive/files/attached-notes"), json=body, auth=True
        )
        return [Note(raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_attached_notes(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        file_id: str,
    ) -> AsyncGenerator[Note, None]:
        body = {
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "fileId": file_id,
        }

        pagination = Pagination[INote](
            self._session,
            Route("POST", "/api/drive/files/attached-notes"),
            json=body,
            auth=True,
        )

        while pagination.is_final is False:
            for raw_note in await pagination.next():
                yield Note(raw_note, client=self._client)

    async def delete(self, *, file_id: str) -> bool:
        """指定したファイルIDのファイルを削除します

        Endpoint: `/api/drive/files/delete`

        Parameters
        ----------
        file_id: str | None
            対象のファイルID, default=None

        Returns
        -------
        bool
            削除に成功したかどうか
        """
        data = {"fileId": file_id}

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/delete"), json=data, auth=True
        )
        return res

    async def update(
        self,
        folder_id: str | None = MISSING,
        name: str | None = MISSING,
        is_sensitive: bool = MISSING,
        comment: str | None = MISSING,
        *,
        file_id: str,
    ) -> File:
        """指定したIDのファイル情報を更新します

        Endpoint: `/api/drive/files/update`

        Parameters
        ----------
        folder_id: str | None
            ファイルを置くフォルダID, default=MISSING
        name: str | None
            ファイル名, default=MISSING
        is_sensitive: bool
            ファイルがセンシティブかどうか, default=MISSING
        comment: str | None
            ファイルのコメント, default=MISSING
        file_id: str | None
            対象のファイルID, default=None

        Returns
        -------
        File
            更新後のファイル
        """
        data = remove_dict_missing(
            {
                "fileId": file_id,
                "folderId": folder_id,
                "name": name,
                "isSensitive": is_sensitive,
                "comment": comment,
            }
        )

        res: IFile = await self._session.request(
            Route("POST", "/api/drive/files/update"), json=data, auth=True
        )
        return File(res, client=self._client)


class ClientFileActions(SharedFileActions):
    def __init__(self, file_ids: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__file_ids: str = file_ids

    @override
    async def get_attached_notes(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        file_id: str | None = None,
    ) -> list[Note]:
        """Get the attached notes of a file

        Endpoint: `/api/drive/files/attached-notes`

        Parameters
        ----------
        since_id: str | None
            The id of the note to start from, defaults to None
        until_id: str | None
            The id of the note to end at, defaults to None
        limit: int
            The amount of notes to get, defaults to 10
        file_id: str | None
            The id of the file to get notes from, defaults to None

        Returns
        -------
        list[Note]
            The attached notes of the file
        """

        file_id = file_id or self.__file_ids

        return await super().get_attached_notes(
            since_id=since_id, until_id=until_id, limit=limit, file_id=file_id
        )

    @override
    async def get_all_attached_notes(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        file_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        file_id = file_id or self.__file_ids

        async for note in super().get_all_attached_notes(
            since_id=since_id, until_id=until_id, limit=limit, file_id=file_id
        ):
            yield note

    @override
    async def delete(self, *, file_id: str | None = None) -> bool:
        """指定したファイルIDのファイルを削除します

        Endpoint: `/api/drive/files/delete`

        Parameters
        ----------
        file_id: str | None
            対象のファイルID, default=None

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        file_id = file_id or self.__file_ids

        return await super().delete(file_id=file_id)

    @override
    async def update(
        self,
        folder_id: str | None = MISSING,
        name: str | None = MISSING,
        is_sensitive: bool = MISSING,
        comment: str | None = MISSING,
        *,
        file_id: str | None = None,
    ) -> File:
        """指定したIDのファイル情報を更新します

        Endpoint: `/api/drive/files/update`

        Parameters
        ----------
        folder_id: str | None
            ファイルを置くフォルダID, default=MISSING
        name: str | None
            ファイル名, default=MISSING
        is_sensitive: bool
            ファイルがセンシティブかどうか, default=MISSING
        comment: str | None
            ファイルのコメント, default=MISSING
        file_id: str | None
            対象のファイルID, default=None

        Returns
        -------
        File
            更新後のファイル
        """
        file_id = file_id or self.__file_ids

        return await super().update(
            folder_id=folder_id,
            name=name,
            is_sensitive=is_sensitive,
            comment=comment,
            file_id=file_id,
        )


class FileActions(SharedFileActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def get_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        type: str | None = None,
        sort: IDriveSort | None = None,
    ) -> list[File]:
        """Get the files of the drive

        Endpoint: `/api/drive/files`

        Parameters
        ----------
        limit: int
            The amount of files to get, defaults to 10
        since_id: str | None
            The id of the file to start from, defaults to None
        until_id: str | None
            The id of the file to end at, defaults to None
        folder_id: str | None
            The id of the folder to get files from, defaults to None
        type: str | None
            The type of file to get, defaults to None
        sort: IDriveSort | None
            The way to sort the files, defaults to None

        Returns
        -------
        list[File]
            The files of the drive
        """

        data = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "folderId": folder_id,
            "type": type,
            "sort": sort,
        }

        raw_files: list[IFile] = await self._session.request(
            Route("POST", "/api/drive/files"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in raw_files]

    async def get_all_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        type: str | None = None,
        sort: IDriveSort | None = None,
    ) -> AsyncGenerator[File, None]:
        body = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "folderId": folder_id,
            "type": type,
            "sort": sort,
        }

        pagination = Pagination[IFile](
            self._session, Route("POST", "/api/drive/files"), json=body, auth=True
        )

        while pagination.is_final is False:
            for raw_file in await pagination.next():
                yield File(raw_file, client=self._client)

    async def check_existence(self, md5: str) -> bool:
        """指定したmd5のファイルが既に存在するか確認します

        Endpoint: `/api/drive/files/check-existence`

        Parameters
        ----------
        md5: str
            確認したいmd5

        Returns
        -------
        bool
            存在するかしないか
        """

        data = {"md5": md5}

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/check-existence"), json=data, auth=True
        )
        return res

    async def create(
        self,
        file: str | bytes | os.PathLike[Any] | io.BufferedIOBase,
        folder_id: str | None = None,
        name: str | None = None,
        comment: str | None = None,
        is_sensitive: bool = False,
        force: bool = False,
    ) -> File:
        """Upload a file to the drive

        Endpoint: `/api/drive/files/create`

        Parameters
        ----------
        file: str | bytes | os.PathLike[Any] | io.BufferedIOBase
            アップロードするファイル
        folder_id: str | None
            アップロード先のフォルダID, default=None
        name: str | None
            ファイルの名前, default=None
        comment: str | None
            ファイルのコメント, default=None
        is_sensitive: bool
            ファイルがセンシティブかどうか, default=False
        force: bool
            ファイルが既に存在する場合でも強制的にアップロードするかどうか, default=False


        Returns
        -------
        File
            アップロードしたファイル
        """

        if isinstance(file, io.IOBase):
            if (file.seekable() and file.readable()) is False:  # 書き込み/読み込みができるか確認
                raise ValueError(f"File buffer {file!r} must be seekable and readable")
            file_byte = file
        elif isinstance(file, bytes):
            file_byte = io.BytesIO(file)
        else:
            file_byte = open(file, "rb")

        data = {
            "folderId": folder_id,
            "name": name,
            "comment": comment,
            "isSensitive": bool_to_string(is_sensitive),
            "force": bool_to_string(force),
            "file": file_byte,
        }
        res: IFile = await self._session.request(
            Route("POST", "/api/drive/files/create"),
            data=data,
            auth=True,
            lower=True,
        )
        return File(res, client=self._client)

    async def find_by_hash(self, md5: str) -> list[File]:
        """指定したハッシュのファイルを検索します

        Endpoint: `/api/drive/files/find-by-hash`

        Parameters
        ----------
        md5: str
            検索したいファイルのハッシュ

        Returns
        -------
        list[File]
            見つかったファイル
        """

        data = {"md5": md5}

        raw_files: list[IFile] = await self._session.request(
            Route("POST", "/api/drive/files/find-by-hash"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in raw_files]

    async def find(self, name: str, folder_id: str | None = None) -> list[File]:
        """指定した名前のファイルを検索します

        Endpoint: `/api/drive/files/find`

        Parameters
        ----------
        name: str
            検索したいファイルの名前
        folder_id: str | None
            ファイルを検索するフォルダID, default=None

        Returns
        -------
        list[File]
            The found files
        """

        data = {"name": name, "folderId": folder_id}

        res: list[IFile] = await self._session.request(
            Route("POST", "/api/drive/files/find"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in res]

    async def show(self, file_id: str, url: str | None = None) -> File:
        """指定したIDのファイル情報を取得します

        Endpoint: `/api/drive/files/show`

        Parameters
        ----------
        file_id: str
            対象のファイルID
        url: str | None
            取得したいファイルのURL, default=None

        Returns
        -------
        File
            取得したファイル
        """

        data = {"fileId": file_id, "url": url}

        res: IFile = await self._session.request(
            Route("POST", "/api/drive/files/show"), json=data, auth=True
        )
        return File(res, client=self._client)

    async def upload_from_url(
        self,
        url: str,
        folder_id: str | None = None,
        is_sensitive: bool = False,
        comment: str | None = None,
        marker: str | None = None,
        force: bool = False,
    ):
        """Upload a file to the drive from a url

        Endpoint: `/api/drive/files/upload-from-url`

        Parameters
        ----------
        url: str
            アップロードするファイルのURL
        folder_id: str | None
            アップロード先のフォルダID, default=None
        is_sensitive: bool
            ファイルがセンシティブかどうか, default=False
        comment: str | None
            ファイルのコメント, default=None
        marker: str | None
            ストリーミング通信でアップロード完了後に区別するためのマーカー, default=None
        force: bool
            同様のファイルが既に存在する場合でも強制的にアップロードするかどうか, default=False

        Returns
        -------
        bool
            アップロードのリクエストに成功したかどうか
        """

        data = {
            "url": url,
            "folderId": folder_id,
            "isSensitive": is_sensitive,
            "comment": comment,
            "marker": marker,
            "force": force,
        }

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/upload-from-url"), json=data, auth=True
        )
        return res
