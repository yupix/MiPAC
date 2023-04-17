from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar
from mipac.types.channel import IChannelLite
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager import ClientManager
    from mipac.manager.channel import ChannelManager
    

T = TypeVar('T', bound=IChannelLite)


class ChannelLite(Generic[T]):
    def __init__(self, channel: T, *, client: ClientManager) -> None:
        self._channel: T = channel
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self._channel['id']

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._channel['created_at'])

    @property
    def last_noted_at(self) -> datetime | None:
        last_noted_at = self._channel.get('last_noted_at')
        return str_to_datetime(last_noted_at) if last_noted_at else None

    @property
    def name(self) -> str:
        return self._channel['name']

    @property
    def description(self) -> str | None:
        return self._channel['description']

    @property
    def user_id(self) -> str:
        return self._channel['user_id']

    @property
    def banner_url(self) -> str | None:
        return self._channel['banner_url']

    @property
    def users_count(self) -> int:
        return self._channel['users_count']

    @property
    def notes_count(self) -> int:
        return self._channel['notes_count']

    @property
    def pinned_note_ids(self) -> list:
        return self._channel.get('pinned_note_ids', [])

    @property
    def api(self) -> ChannelManager:
        return self.__client._create_channel_instance(channel_id=self.id)
