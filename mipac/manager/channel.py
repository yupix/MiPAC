
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.channel import ChannelActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ChannelManager(AbstractManager):
    def __init__(self, channel_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__channel_id: str | None = channel_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ChannelActions:
        return ChannelActions(channel_id=self.__channel_id, session=self.__session, client=self.__client)
