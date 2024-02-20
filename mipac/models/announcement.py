from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.types.announcement import (
    AnnoucementDisplay,
    AnnoucementIcon,
    IAnnouncement,
    IAnnouncementDetailed,
)
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.admins.announcement import ClientAdminAnnouncementManager
    from mipac.manager.client import ClientManager


class Announcement:
    def __init__(self, announcement: IAnnouncement, *, client: ClientManager) -> None:
        self.__announcement: IAnnouncement = announcement
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
    def icon(self) -> AnnoucementIcon:
        return self.__announcement["icon"]

    @property
    def display(self) -> AnnoucementDisplay:
        return self.__announcement["display"]

    @property
    def need_confirmation_to_read(self) -> bool:
        return self.__announcement["need_confirmation_to_read"]

    @property
    def silence(self) -> bool:
        return self.__announcement["silence"]

    @property
    def for_you(self) -> bool:
        return self.__announcement["for_you"]

    @property
    def is_read(self) -> bool | None:
        return self.__announcement.get("is_read")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Announcement) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    @property
    def api(self) -> ClientAdminAnnouncementManager:
        return self.__client.admin._create_client_announcement_manager(announce_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self.__announcement.get(key)


class AnnouncementDetailed:
    def __init__(self, raw_announcement: IAnnouncementDetailed, *, client: ClientManager) -> None:
        self.__raw_announcement: IAnnouncementDetailed = raw_announcement
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_announcement["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__raw_announcement["created_at"])

    @property
    def updated_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__raw_announcement["updated_at"])
            if self.__raw_announcement["updated_at"]
            else None
        )

    @property
    def title(self) -> str:
        return self.__raw_announcement["title"]

    @property
    def text(self) -> str:
        return self.__raw_announcement["text"]

    @property
    def image_url(self) -> str | None:
        return self.__raw_announcement["image_url"]

    @property
    def icon(self) -> AnnoucementIcon:
        return self.__raw_announcement["icon"]

    @property
    def display(self) -> AnnoucementDisplay:
        return self.__raw_announcement["display"]

    @property
    def is_active(self) -> bool:
        return self.__raw_announcement["is_active"]

    @property
    def for_existing_users(self) -> bool:
        return self.__raw_announcement["for_existing_users"]

    @property
    def silence(self) -> bool:
        return self.__raw_announcement["silence"]

    @property
    def need_confirmation_to_read(self) -> bool:
        return self.__raw_announcement["need_confirmation_to_read"]

    @property
    def user_id(self) -> str | None:
        return self.__raw_announcement["user_id"]

    @property
    def reads(self) -> int:
        """Returns the number of reads of the announcement."""
        return self.__raw_announcement["reads"]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, AnnouncementDetailed) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    @property
    def api(self) -> ClientAdminAnnouncementManager:
        return self.__client.admin._create_client_announcement_manager(announce_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self.__raw_announcement.get(key)
