from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, Literal, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.models.announcement import Announcement
from mipac.models.lite.user import BadgeRole, LiteUser
from mipac.models.note import Note
from mipac.types.page import IPage
from mipac.types.user import (
    IAchievement,
    IBlockingUser,
    IMeDetailed,
    IUserDetailed,
    IUserDetailedField,
    IUserRole,
)
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ("UserDetailed", "LiteUser", "Achievement", "BlockingUser", "MeDetailed")

T = TypeVar("T", bound=IUserDetailed)


class BlockingUser(AbstractModel):
    def __init__(self, blocking_user_data: IBlockingUser, *, client: ClientManager) -> None:
        self.__blocking_user_data: IBlockingUser = blocking_user_data
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__blocking_user_data["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__blocking_user_data["created_at"])

    @property
    def blockee_id(self) -> str:
        return self.__blocking_user_data["blockee_id"]

    @property
    def blockee(self) -> UserDetailed:
        return UserDetailed(self.__blocking_user_data["blockee"], client=self.__client)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, BlockingUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class Achievement(AbstractModel):
    def __init__(self, detail: IAchievement):
        self.__detail: IAchievement = detail

    @property
    def name(self) -> str:
        return self.__detail["name"]

    @property
    def unlocked_at(self) -> int:
        return self.__detail["unlocked_at"]


class UserRole(BadgeRole[IUserRole]):
    def __init__(self, data: IUserRole, *, client: ClientManager) -> None:
        super().__init__(data, client=client)

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def color(self) -> str | None:
        return self._data["color"]

    @property
    def description(self) -> str:
        return self._data["description"]

    @property
    def is_moderator(self) -> bool:
        return self._data["is_moderator"]

    @property
    def is_administrator(self) -> bool:
        return self._data["is_administrator"]


class UserDetailed(LiteUser[T], Generic[T]):
    __slots__ = ("__client",)

    def __init__(self, user: T, *, client: ClientManager):
        super().__init__(user=user, client=client)

    @property
    def achievements(self) -> list[Achievement]:
        return [Achievement(i) for i in self._user.get("achievements", [])]

    @property
    def fields(self) -> list[IUserDetailedField]:
        return self._user["fields"]

    @property
    def followers_count(self) -> int:
        return self._user["followers_count"]

    @property
    def following_count(self) -> int:
        return self._user["following_count"]

    @property
    def has_pending_follow_request_from_you(self) -> bool | None:
        return self._user.get("has_pending_follow_request_from_you")

    @property
    def has_pending_follow_request_to_you(self) -> bool | None:
        return self._user.get("has_pending_follow_request_to_you")

    @property
    def is_admin(self) -> bool:
        return self._user["is_admin"]

    @property
    def is_blocked(self) -> bool | None:
        return self._user.get("is_blocked")

    @property
    def is_blocking(self) -> bool | None:
        return self._user.get("is_blocking")

    @property
    def is_bot(self) -> bool:
        return self._user["is_bot"]

    @property
    def is_cat(self) -> bool:
        return self._user["is_cat"]

    @property
    def is_followed(self) -> bool | None:
        return self._user.get("is_followed")

    @property
    def is_following(self) -> bool | None:
        return self._user.get("is_following")

    @property
    def is_locked(self) -> bool:
        return self._user["is_locked"]

    @property
    def is_moderator(self) -> bool:
        return self._user["is_moderator"]

    @property
    def is_muted(self) -> bool | None:
        return self._user.get("is_muted")

    @property
    def is_silenced(self) -> bool:
        return self._user["is_silenced"]

    @property
    def is_suspended(self) -> bool:
        return self._user["is_suspended"]

    @property
    def public_reactions(self) -> bool:
        return self._user["public_reactions"]

    @property
    def security_keys(self) -> bool:
        return self._user["security_keys"]

    @property
    def two_factor_enabled(self) -> bool:
        return self._user["two_factor_enabled"]

    @property
    def notes_count(self) -> int:
        return self._user["notes_count"]

    @property
    def pinned_note_ids(self) -> list[str]:
        return self._user["pinned_note_ids"]

    @property
    def pinned_notes(self) -> list[Note]:
        return [Note(i, client=self.__client) for i in self._user["pinned_notes"]]

    @property
    def banner_blurhash(self) -> str | None:
        return self._user.get("banner_blurhash")

    @property
    def banner_color(self) -> str | None:
        return self._user.get("banner_color")

    @property
    def banner_url(self) -> str | None:
        return self._user.get("banner_url")

    @property
    def birthday(self) -> str | None:
        return self._user.get("birthday")

    @property
    def created_at(self) -> str | None:
        return self._user.get("created_at")

    @property
    def description(self) -> str | None:
        return self._user.get("description")

    @property
    def ff_visibility(
        self,
    ) -> Literal["public", "followers", "private"] | None:
        return self._user.get("ff_visibility")

    @property
    def lang(self) -> str | None:
        return self._user.get("lang")

    @property
    def last_fetched_at(self) -> str | None:
        return self._user.get("last_fetched_at")

    @property
    def location(self) -> str | None:
        return self._user.get("location")

    @property
    def logged_in_days(self) -> int | None:
        return self._user.get("logged_in_days")

    @property
    def pinned_page(self) -> IPage | None:
        return self._user.get("pinned_page")

    @property
    def pinned_page_id(self) -> str | None:
        return self._user.get("pinned_page_id")

    @property
    def updated_at(self) -> str | None:
        return self._user.get("updated_at")

    @property
    def uri(self) -> str | None:
        return self._user.get("uri")

    @property
    def url(self) -> str | None:
        return self._user.get("url")

    @property
    def use_password_less_login(self) -> bool | None:
        return self._user.get("use_password_less_login")

    @property
    def roles(self) -> list[UserRole]:
        return [UserRole(i, client=self.__client) for i in self._user.get("roles", [])]

    @property
    def memo(self) -> str | None:
        return self._user.get("memo")

    @property
    def moderation_note(self) -> str | None:
        return self._user.get("moderation_note")


class MeDetailed(UserDetailed[IMeDetailed]):
    def __init__(self, data: IMeDetailed, *, client: ClientManager):
        super().__init__(data, client=client)

    @property
    def avatar_id(self) -> str:
        return self._user["avatar_id"]

    @property
    def banner_id(self) -> str:
        return self._user["banner_id"]

    @property
    def auto_accept_followed(self) -> bool:
        return self._user["auto_accept_followed"]

    @property
    def always_mark_nsfw(self) -> bool:
        return self._user["always_mark_nsfw"]

    @property
    def careful_bot(self) -> bool:
        return self._user["careful_bot"]

    @property
    def email_notification_types(self) -> list[str]:
        return self._user["email_notification_types"]

    @property
    def has_pending_received_follow_request(self) -> bool:
        return self._user["has_pending_received_follow_request"]

    @property
    def has_unread_announcement(self) -> bool:
        return self._user["has_unread_announcement"]

    @property
    def has_unread_antenna(self) -> bool:
        return self._user["has_unread_antenna"]

    @property
    def has_unread_mentions(self) -> bool:
        return self._user["has_unread_mentions"]

    @property
    def has_unread_messaging_message(self) -> bool:
        return self._user["has_unread_messaging_message"]

    @property
    def has_unread_notification(self) -> bool:
        return self._user["has_unread_notification"]

    @property
    def has_unread_specified_notes(self) -> bool:
        return self._user["has_unread_specified_notes"]

    @property
    def hide_online_status(self) -> bool:
        return self._user["hide_online_status"]

    @property
    def inject_featured_note(self) -> bool:
        return self._user["inject_featured_note"]

    @property
    def integrations(self) -> dict[str, str]:
        return self._user["integrations"]

    @property
    def is_deleted(self) -> bool:
        return self._user["is_deleted"]

    @property
    def is_explorable(self) -> bool:
        return self._user["is_explorable"]

    @property
    def muted_words(self) -> list[list[str]]:
        return self._user["muted_words"]

    @property
    def muting_notification_types(self) -> list[str]:
        return self._user["muting_notification_types"]

    @property
    def no_crawle(self) -> bool:
        return self._user["no_crawle"]

    @property
    def receive_announcement_email(self) -> bool:
        return self._user["receive_announcement_email"]

    @property
    def use_password_less_login(self) -> bool:
        return self._user["use_password_less_login"]

    @property
    def unread_announcements(self) -> list[Announcement]:
        return [
            Announcement(announcement, client=self.__client)
            for announcement in self._user["unread_announcements"]
        ]

    @property
    def two_factor_backup_codes_stock(self) -> Literal["full", "partial", "none"]:
        return self._user["two_factor_backup_codes_stock"]
