from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING

from mipac.types.announcement import IAnnouncement
from mipac.util import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Announcement:
    def __init__(
        self, announcement: IAnnouncement, *, client: ClientManager
    ) -> None:
        self.__announcement: IAnnouncement = announcement
        self.__client: ClientManager = client

    @property
    def id(self) -> str | None:
        return self.__announcement['id']

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__announcement['created_at'])

    @property
    def updated_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__announcement['updated_at'])
            if self.__announcement['updated_at']
            else None
        )

    @property
    def text(self) -> str:
        return self.__announcement['text']

    @property
    def title(self) -> str:
        return self.__announcement['title']

    @property
    def image_url(self) -> str | None:
        return self.__announcement['image_url']

    @property
    def is_read(self) -> bool:
        return self.__announcement['is_read']
