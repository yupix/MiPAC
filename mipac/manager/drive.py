from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.drive import (
    ClientFileActions,
    ClientFolderActions,
    DriveActions,
    FileActions,
    FolderActions,
)
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ["FolderManager", "FileManager", "DriveManager"]


class ClientFileManager(AbstractManager):
    def __init__(
        self,
        file_id: str | None = None,
        folder_id: str | None = None,
        url: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__file_id: str | None = file_id
        self.__folder_id: str | None = folder_id
        self.__url: str | None = url

    @property
    def action(self) -> ClientFileActions:
        return ClientFileActions(
            file_id=self.__file_id,
            folder_id=self.__folder_id,
            url=self.__url,
            client=self.__client,
            session=self.__session,
        )


class FileManager(AbstractManager):
    def __init__(
        self,
        file_id: str | None = None,
        folder_id: str | None = None,
        url: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__file_id = file_id
        self.__folder_id: str | None = folder_id
        self.__url: str | None = url

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
            folder_id=self.__folder_id,
            url=self.__url,
            client=self.__client,
            session=self.__session,
        )


class ClientFolderManager(AbstractManager):
    def __init__(
        self, folder_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        self.__folder_id = folder_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.file: FileManager = FileManager(folder_id=folder_id, session=session, client=client)

    @property
    def action(self) -> ClientFolderActions:
        """
        フォルダーの操作を行うインスタンスを返します

        Returns
        -------
        FolderActions
            フォルダーに対するアクション
        """
        return ClientFolderActions(
            folder_id=self.__folder_id,
            session=self.__session,
            client=self.__client,
        )


class FolderManager(AbstractManager):
    def __init__(
        self, folder_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        self.__folder_id = folder_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.file: FileManager = FileManager(folder_id=folder_id, session=session, client=client)

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
            file_id=file_id,
            folder_id=self.__folder_id,
            session=self.__session,
            client=self.__client,
        )


class DriveManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.folder: FolderManager = FolderManager(session=session, client=client)
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
        return FolderManager(session=self.__session, client=self.__client, folder_id=folder_id)

    def _get_client_folder_instance(self, folder_id: str) -> ClientFolderManager:
        return ClientFolderManager(
            folder_id=folder_id, session=self.__session, client=self.__client
        )

    def _get_client_file_instance(
        self, *, file_id: str, url: str, folder_id: str | None = None
    ) -> ClientFileManager:
        return ClientFileManager(
            file_id=file_id,
            folder_id=folder_id,
            url=url,
            session=self.__session,
            client=self.__client,
        )
