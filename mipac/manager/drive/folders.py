from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.drive.folders import (
    ClientFileActionsInFolder,
    ClientFolderActions,
    FolderActions,
)
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientFolderManager(AbstractManager):
    def __init__(self, folder_id: str, *, session: HTTPClient, client: ClientManager):
        self.__folder_id: str = folder_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientFolderActions = ClientFolderActions(
            folder_id=folder_id, session=session, client=client
        )
        self.files = ClientFileActionsInFolder(folder_id=folder_id, session=session, client=client)

    @property
    def action(self) -> ClientFolderActions:
        return self.__action


class FolderManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: FolderActions = FolderActions(session=session, client=client)

    @property
    def action(self) -> FolderActions:
        return self.__action
