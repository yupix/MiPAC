from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.http import HTTPClient
from mipac.abstract.action import AbstractAction

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientFolderActions(AbstractAction):
    def __init__(self, folder_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__folder_id: str | None = folder_id
        self._session: HTTPClient = session
        self._client: ClientManager = client


class FolderActions(ClientFolderActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

