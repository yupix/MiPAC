from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.models.announcement import Announcement
from mipac.models.lite.user import BadgeRole, PartialUser
from mipac.models.note import Note
from mipac.types.page import IPage
from mipac.config import config
from mipac.types.user import (
    IAchievement,
    IBlockingUser,
    IFfVisibility,
    IMeDetailed,
    IMeDetailedModerator,
    IUser,
    IUserDetailed,
    IUserDetailedModerator,
    IUserDetailedNotLogined,
    IUserField,
    IUserNotify,
    IUserRole,
    is_me_detailed,
    is_me_detailed_moderator,
    is_user_detailed,
    is_user_detailed_moderator,
    is_user_detailed_not_logined,
)
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ("UserDetailed", "PartialUser", "Achievement", "BlockingUser", "MeDetailed")

T = TypeVar("T", bound=IUserDetailedNotLogined)
U = TypeVar("U", bound=IUserDetailed)
M = TypeVar("M", bound=IMeDetailed)


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


class UserDetailedNotLogined(PartialUser[T], Generic[T]):
    def __init__(self, raw_user: T, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)

    @property
    def url(self) -> str | None:
        return self._raw_user["url"]

    @property
    def uri(self) -> str | None:
        return self._raw_user["uri"]

    @property
    def moved_to(self) -> str | None:
        return self._raw_user["moved_to"]

    @property
    def also_known_as(self) -> list[str] | None:
        return self._raw_user["also_known_as"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._raw_user["created_at"])

    @property
    def updated_at(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_user["updated_at"]) if self._raw_user["updated_at"] else None
        )

    @property
    def last_fetched_at(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_user["last_fetched_at"])
            if self._raw_user["last_fetched_at"]
            else None
        )

    @property
    def banner_url(self) -> str | None:
        return self._raw_user["banner_url"]

    @property
    def banner_blurhash(self) -> str | None:
        return self._raw_user["banner_blurhash"]

    @property
    def is_locked(self) -> bool:
        return self._raw_user["is_locked"]

    @property
    def is_silenced(self) -> bool:
        return self._raw_user["is_silenced"]

    @property
    def is_suspended(self) -> bool:
        return self._raw_user["is_suspended"]

    @property
    def description(self) -> str | None:
        return self._raw_user["description"]

    @property
    def location(self) -> str | None:
        return self._raw_user["location"]

    @property
    def birthday(self) -> str | None:
        return self._raw_user["birthday"]

    @property
    def lang(self) -> str | None:
        return self._raw_user["lang"]

    @property
    def fields(self) -> list[IUserField]:  # TODO: モデル化
        return self._raw_user["fields"]

    @property
    def verified_links(self) -> list[str]:
        return self._raw_user["verified_links"]

    @property
    def followers_count(self) -> int:
        return self._raw_user["followers_count"]

    @property
    def following_count(self) -> int:
        return self._raw_user["following_count"]

    @property
    def notes_count(self) -> int:
        return self._raw_user["notes_count"]

    @property
    def pinned_note_ids(self) -> list[str]:
        return self._raw_user["pinned_note_ids"]

    @property
    def pinned_notes(self) -> list[Note]:
        return [Note(raw_note, client=self._client) for raw_note in self._raw_user["pinned_notes"]]

    @property
    def pinned_page_id(self) -> str | None:
        return self._raw_user["pinned_page_id"]

    @property
    def pinned_page(self) -> IPage | None:  # TODO: モデルに
        return self._raw_user["pinned_page"]

    @property
    def public_reactions(self) -> bool:
        return self._raw_user["public_reactions"]

    @property
    def ff_visibility(self) -> IFfVisibility:
        return self._raw_user["ff_visibility"]

    @property
    def two_factor_enabled(self) -> bool:
        return self._raw_user["two_factor_enabled"]

    @property
    def use_password_less_login(self) -> bool:
        return self._raw_user["use_password_less_login"]

    @property
    def security_keys(self) -> bool:
        return self._raw_user["security_keys"]

    @property
    def roles(self) -> list[UserRole]:
        return [UserRole(raw_role, client=self._client) for raw_role in self._raw_user["roles"]]

    @property
    def memo(self) -> str | None:
        return self._raw_user["memo"]

    # TODO: 比較演算子が必要かちょっと後で確認する


class UserDetailed(UserDetailedNotLogined[U], Generic[U]):
    def __init__(self, raw_user: U, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)

    @property
    def is_following(self) -> bool:
        return self._raw_user["is_following"]

    @property
    def is_followed(self) -> bool:
        return self._raw_user["is_followed"]

    @property
    def has_pending_follow_request_from_you(self) -> bool:
        return self._raw_user["has_pending_follow_request_from_you"]

    @property
    def has_pending_follow_request_to_you(self) -> bool:
        return self._raw_user["has_pending_follow_request_to_you"]

    @property
    def is_blocking(self) -> bool:
        return self._raw_user["is_blocking"]

    @property
    def is_blocked(self) -> bool:
        return self._raw_user["is_blocked"]

    @property
    def is_muted(self) -> bool:
        return self._raw_user["is_muted"]

    @property
    def is_renote_muted(self) -> bool:
        return self._raw_user["is_renote_muted"]

    @property
    def notify(self) -> IUserNotify:
        return self._raw_user["notify"]


class UserDetailedModerator(UserDetailed[IUserDetailedModerator]):
    def __init__(self, raw_user: IUserDetailedModerator, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)

    @property
    def moderation_note(self) -> str:
        return self._raw_user["moderation_note"]


class MeDetailed(UserDetailed[M], Generic[M]):
    def __init__(self, raw_user: M, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)

    @property
    def avatar_id(self) -> str:
        return self._raw_user["avatar_id"]

    @property
    def banner_id(self) -> str | None:
        return self._raw_user["banner_id"]

    @property
    def is_moderator(self) -> bool:
        return self._raw_user["is_moderator"]

    @property
    def is_admin(self) -> bool:
        return self._raw_user["is_admin"]

    @property
    def inject_featured_note(self) -> bool:
        return self._raw_user["inject_featured_note"]

    @property
    def receive_announcement_email(self) -> bool:
        return self._raw_user["receive_announcement_email"]

    @property
    def always_mark_nsfw(self) -> bool:
        return self._raw_user["always_mark_nsfw"]

    @property
    def auto_sensitive(self) -> bool:
        return self._raw_user["auto_sensitive"]

    @property
    def careful_bot(self) -> bool:
        return self._raw_user["careful_bot"]

    @property
    def auto_accept_followed(self) -> bool:
        return self._raw_user["auto_accept_followed"]

    @property
    def no_crawle(self) -> bool:
        return self._raw_user["no_crawle"]

    @property
    def prevent_ai_learning(self) -> bool:
        return self._raw_user["prevent_ai_learning"]

    @property
    def is_explorable(self) -> bool:
        return self._raw_user["is_explorable"]

    @property
    def is_deleted(self) -> bool:
        return self._raw_user["is_deleted"]

    @property
    def two_factor_backup_codes_stock(self) -> str:
        return self._raw_user["two_factor_backup_codes_stock"]

    @property
    def hide_online_status(self) -> bool:
        return self._raw_user["hide_online_status"]

    @property
    def has_unread_specified_notes(self) -> bool:
        return self._raw_user["has_unread_specified_notes"]

    @property
    def has_unread_mentions(self) -> bool:
        return self._raw_user["has_unread_mentions"]

    @property
    def has_unread_announcement(self) -> bool:
        return self._raw_user["has_unread_announcement"]

    @property
    def unread_announcements(self) -> Announcement:
        return Announcement(self._raw_user["unread_announcements"], client=self._client)

    @property
    def has_unread_antenna(self) -> bool:
        return self._raw_user["has_unread_antenna"]

    @property
    def has_unread_channel(self) -> bool:
        return self._raw_user["has_unread_channel"]

    @property
    def has_unread_notification(self) -> bool:
        return self._raw_user["has_unread_notification"]

    @property
    def has_pending_received_follow_request(self) -> bool:
        return self._raw_user["has_pending_received_follow_request"]

    @property
    def muted_words(self) -> list[str]:
        return self._raw_user["muted_words"]

    @property
    def muted_instances(self) -> dict:
        return self._raw_user["muted_instances"]

    @property
    def muting_notification_types(self) -> dict:
        return self._raw_user["muting_notification_types"]

    @property
    def notification_recieve_config(self) -> dict:
        return self._raw_user["notification_recieve_config"]

    @property
    def email_notification_types(self) -> dict:
        return self._raw_user["email_notification_types"]

    @property
    def achievements(self) -> dict:
        return self._raw_user["achievements"]

    @property
    def logged_in_days(self) -> int:
        return self._raw_user["logged_in_days"]

    @property
    def policies(self) -> dict:
        return self._raw_user["policies"]


class MeDetailedModerator(MeDetailed):
    def __init__(self, raw_user: IMeDetailedModerator, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)

    @property
    def moderation_note(self) -> str:
        return self._raw_user["moderation_note"]


def create_user_model(
    user: IUser, client: ClientManager
) -> (
    MeDetailed[IMeDetailed]
    | UserDetailedNotLogined[IUserDetailedNotLogined]
    | UserDetailed[IUserDetailed]
    | UserDetailedModerator
    | MeDetailedModerator
):
    if is_user_detailed_not_logined(user):  # ログインしてないやつを最優先に返す
        return UserDetailedNotLogined(user, client=client)
    if is_me_detailed_moderator(user, config.account_id):  # 自身でモデレーターが2
        return MeDetailedModerator(user, client=client)
    if is_me_detailed(user, config.account_id):  # 自身が3
        return MeDetailed(user, client=client)
    if is_user_detailed_moderator(user):  # 他人でモデレーター視点が4
        return UserDetailedModerator(user, client=client)
    if is_user_detailed(user):  # 他人が5
        return UserDetailed(user, client=client)

    
    raise ValueError("Invalid user model")
