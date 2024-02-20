from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.channel import ChannelActions, ClientChannelActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientChannelManager(AbstractManager):
    def __init__(self, channel_id: str, *, session: HTTPClient, client: ClientManager):
        self._channel_id: str = channel_id
        self._session: HTTPClient = session
        self._client: ClientManager = client
        self._action: ClientChannelActions = ClientChannelActions(
            channel_id=channel_id, session=session, client=client
        )

    @property
    def action(self) -> ClientChannelActions:
        return self._action


class ChannelManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ChannelActions = ChannelActions(
            session=self.__session, client=self.__client
        )

    @property
    def action(self) -> ChannelActions:
        return self.__action
