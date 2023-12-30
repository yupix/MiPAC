from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.drive.files import ClientFileActions, FileActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientFileManager(AbstractManager):
    def __init__(self, file_id: str, *, session: HTTPClient, client: ClientManager):
        self.__file_id: str = file_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientFileActions = ClientFileActions(
            file_ids=file_id, session=session, client=client
        )

    @property
    def action(self) -> ClientFileActions:
        return self.__action


class DriveFileManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: FileActions = FileActions(session=session, client=client)

    @property
    def action(self) -> FileActions:
        return self.__action
