from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.types.channel import IChannel

if TYPE_CHECKING:
    from mipac.manager import ClientActions


class Channel:
    def __init__(self, channel: IChannel, *, client: ClientActions) -> None:
        self.__channel: IChannel = channel
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__channel['id']

    @property
    def created_at(self) -> str:
        return self.__channel['created_at']

    @property
    def last_noted_at(self) -> str:
        return self.__channel['last_noted_at']

    @property
    def name(self) -> str:
        return self.__channel['name']

    @property
    def description(self) -> str | None:
        return self.__channel['description']

    @property
    def banner_url(self) -> str | None:
        return self.__channel['banner_url']

    @property
    def notes_count(self) -> int:
        return self.__channel['notes_count']

    @property
    def users_count(self) -> int:
        return self.__channel['users_count']

    @property
    def is_following(self) -> bool:
        return bool(self.__channel['is_following'])

    @property
    def user_id(self) -> str:
        return self.__channel['user_id']

    @property
    def has_unread_note(self) -> bool:
        return self.__channel['has_unread_note']
