from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.drive.drive import DriveActions
from mipac.http import HTTPClient
from mipac.manager.drive.files import ClientFileManager, DriveFileManager
from mipac.manager.drive.folders import ClientFolderManager, FolderManager

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class DriveManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: DriveActions = DriveActions(session=session, client=client)
        self.files: DriveFileManager = DriveFileManager(session=session, client=client)
        self.folders: FolderManager = FolderManager(session=session, client=client)

    @property
    def action(self) -> DriveActions:
        return self.__action

    def _create_client_file_manager(self, *, file_id: str) -> ClientFileManager:
        return ClientFileManager(file_id=file_id, session=self.__session, client=self.__client)

    def _create_client_folder_manager(self, *, folder_id: str) -> ClientFolderManager:
        return ClientFolderManager(
            folder_id=folder_id, session=self.__session, client=self.__client
        )
