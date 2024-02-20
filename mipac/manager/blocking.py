from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.blocking import BlockingActions, ClientBlockingActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientBlockingManager(BlockingActions):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        self.__action: ClientBlockingActions = ClientBlockingActions(
            user_id=user_id, session=session, client=client
        )

    @property
    def action(self) -> ClientBlockingActions:
        return self.__action


class BlockingManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: BlockingActions = BlockingActions(session=session, client=client)

    @property
    def action(self) -> BlockingActions:
        return self.__action
