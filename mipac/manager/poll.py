from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.poll import ClientPollActions, PollActions

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class ClientPollManager(AbstractManager):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientPollActions = ClientPollActions(
            note_id=self.__note_id, session=self.__session, client=self.__client
        )

    @property
    def action(self) -> ClientPollActions:
        return self.__action


class PollManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: PollActions = PollActions(session=self.__session, client=self.__client)

    @property
    def action(self) -> PollActions:
        return self.__action
