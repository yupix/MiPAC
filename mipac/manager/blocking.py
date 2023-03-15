from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.blocking import BlockingActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class BlockingManager(AbstractManager):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> BlockingActions:
        return BlockingActions(
            user_id=self.__user_id, session=self.__session, client=self.__client
        )
