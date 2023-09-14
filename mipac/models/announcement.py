from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.types.announcement import IAnnouncement, IAnnouncementCommon, IAnnouncementSystem
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.actions.admins.announcement import AdminAnnouncementClientActions
    from mipac.manager.client import ClientManager

T = TypeVar("T", bound=IAnnouncementCommon)


class AnnouncementCommon(Generic[T], AbstractModel):
    def __init__(self, announcement: T, *, client: ClientManager) -> None:
        self.__announcement: T = announcement
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__announcement["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__announcement["created_at"])

    @property
    def updated_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__announcement["updated_at"])
            if self.__announcement["updated_at"]
            else None
        )

    @property
    def text(self) -> str:
        return self.__announcement["text"]

    @property
    def title(self) -> str:
        return self.__announcement["title"]

    @property
    def image_url(self) -> str | None:
        return self.__announcement["image_url"]

    @property
    def action(self) -> AdminAnnouncementClientActions:
        return self.__client.admin.announcement._create_client_announcement_instance(
            announce_id=self.id
        )

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Announcement) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class Announcement(AnnouncementCommon):
    def __init__(self, announcement: IAnnouncement, *, client: ClientManager) -> None:
        super().__init__(announcement, client=client)
        self.__announcement: IAnnouncement

    @property
    def is_read(self) -> bool:
        return self.__announcement["is_read"]


class AnnouncementSystem(AnnouncementCommon):
    def __init__(self, announcement: IAnnouncementSystem, *, client: ClientManager) -> None:
        super().__init__(announcement, client=client)
        self.__announcement: IAnnouncementSystem

    @property
    def reads(self) -> int:
        return self.__announcement["reads"]
