from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.abc.manager import AbstractManager
from mipac.actions.drive import DriveActions, FileActions, FolderActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ['FolderManager', 'FileManager', 'DriveManager']


class FileManager(AbstractManager):
    def __init__(
        self,
        file_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.__file_id = file_id

    @property
    def action(self) -> FileActions:
        """
        ファイルの操作を行うインスタンスを返します

        Return
        ------
        FileActions
            ファイルに対するアクション
        """
        return FileActions(
            file_id=self.__file_id,
            client=self.__client,
            session=self.__session,
        )


class FolderManager(AbstractManager):
    def __init__(
        self,
        folder_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__folder_id = folder_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.file: FileManager = FileManager(session=session, client=client)

    @property
    def action(self) -> FolderActions:
        """
        フォルダーの操作を行うインスタンスを返します

        Returns
        -------
        FolderActions
            フォルダーに対するアクション
        """
        return FolderActions(
            folder_id=self.__folder_id,
            session=self.__session,
            client=self.__client,
        )

    def _get_file_instance(self, file_id: str) -> FileManager:
        return FileManager(
            file_id=file_id, session=self.__session, client=self.__client
        )


class DriveManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.folder: FolderManager = FolderManager(
            session=session, client=client
        )
        self.file: FileManager = FileManager(session=session, client=client)

    @property
    def action(self) -> DriveActions:
        """
        ドライブの操作を行うインスタンスを返します

        Returns
        -------
        DriveActions
            ドライブに対するアクション
        """
        return DriveActions(client=self.__client, session=self.__session)

    def _get_folder_instance(self, folder_id: str) -> FolderManager:
        return FolderManager(
            session=self.__session, client=self.__client, folder_id=folder_id
        )
