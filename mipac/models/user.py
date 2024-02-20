from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.announcement import Announcement
from mipac.models.lite.role import PartialRole
from mipac.models.lite.user import BadgeRole, PartialUser
from mipac.models.note import Note
from mipac.types.follow import IFederationFollowCommon, IFederationFollower, IFederationFollowing
from mipac.types.meta import IPolicies
from mipac.types.page import IPage
from mipac.types.user import (
    EmailNotificationTypes,
    GetFrequentlyRepliedUsersResponse,
    IAchievement,
    IFfVisibility,
    IMeDetailedOnlySchema,
    IMeDetailedSchema,
    ITwoFactorBackupCodesStock,
    IUser,
    IUserDetailedNotMeOnlySchema,
    IUserDetailedNotMeSchema,
    IUserField,
    IUserList,
    IUserListMembership,
    IUserNotify,
    IUserRole,
    IUserSecurityKey,
    NotificationRecieveConfig,
    is_me_detailed,
    is_user_detailed_not_me,
)
from mipac.utils.format import str_to_datetime
from mipac.utils.util import DeprecatedClass

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.users.list import ClientUserListManager


__all__ = ("PartialUser", "Achievement", "MeDetailed")


class FollowCommon[FFC: IFederationFollowCommon]:
    def __init__(self, raw_follow: FFC, *, client: ClientManager) -> None:
        self._raw_follow: FFC = raw_follow
        self._client: ClientManager = client

    @property
    def id(self) -> str:
        return self._raw_follow["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._raw_follow["created_at"])

    @property
    def follower_id(self) -> str:
        return self._raw_follow["follower_id"]

    @property
    def follower(self) -> UserDetailedNotMe | None:
        raw_follower = self._raw_follow.get("follower")
        return packed_user(raw_follower, client=self._client) if raw_follower else None

    @property
    def followee_id(self) -> str:
        return self._raw_follow["followee_id"]

    @property
    def followee(self) -> UserDetailedNotMe | None:
        raw_followee = self._raw_follow.get("followee")
        return packed_user(raw_followee, client=self._client) if raw_followee else None

    def _get(self, key: str) -> Any | None:
        return self._raw_follow.get(key)


class Follower(FollowCommon[IFederationFollower]):
    def __init__(self, raw_follow: IFederationFollower, *, client: ClientManager) -> None:
        super().__init__(raw_follow=raw_follow, client=client)


class Following(FollowCommon[IFederationFollowing]):
    def __init__(self, raw_following: IFederationFollowing, *, client: ClientManager) -> None:
        super().__init__(raw_follow=raw_following, client=client)


class Achievement:
    def __init__(self, detail: IAchievement):
        self.__detail: IAchievement = detail

    @property
    def name(self) -> str:
        return self.__detail["name"]

    @property
    def unlocked_at(self) -> int:
        return self.__detail["unlocked_at"]

    def _get(self, key: str) -> Any | None:
        return self.__detail.get(key)


class UserField:
    def __init__(self, raw_user_field: IUserField, *, client: ClientManager) -> None:
        self._raw_user_field: IUserField = raw_user_field
        self.__client: ClientManager = client

    @property
    def name(self) -> str:
        return self._raw_user_field["name"]

    @property
    def value(self) -> str:
        return self._raw_user_field["value"]

    def _get(self, key: str) -> Any | None:
        return self._raw_user_field.get(key)


@DeprecatedClass(remove_in_version="0.7.0")
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


class UserDetailedNotMeOnly:
    def __init__(self, raw_user: IUserDetailedNotMeOnlySchema, *, client: ClientManager) -> None:
        self._raw_user: IUserDetailedNotMeOnlySchema = raw_user
        self._client: ClientManager = client

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
    def fields(self) -> list[UserField]:
        return [UserField(i, client=self._client) for i in self._raw_user["fields"]]

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
    def following_visibility(self) -> IFfVisibility:
        return self._raw_user["following_visibility"]

    @property
    def followers_visibility(self) -> IFfVisibility:
        return self._raw_user["followers_visibility"]

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
    def roles(self) -> list[PartialRole]:
        return [PartialRole(i, client=self._client) for i in self._raw_user["roles"]]

    @property
    def memo(self) -> str | None:
        return self._raw_user["memo"]

    @property
    def moderation_note(self) -> str | None:
        return self._raw_user.get("moderation_note")

    @property
    def is_following(self) -> bool | None:
        return self._raw_user.get("is_following")

    @property
    def is_followed(self) -> bool | None:
        return self._raw_user.get("is_followed")

    @property
    def has_pending_follow_request_from_you(self) -> bool | None:
        return self._raw_user.get("has_pending_follow_request_from_you")

    @property
    def has_pending_follow_request_to_you(self) -> bool | None:
        return self._raw_user.get("has_pending_follow_request_to_you")

    @property
    def is_blocking(self) -> bool | None:
        return self._raw_user.get("is_blocking")

    @property
    def is_blocked(self) -> bool | None:
        return self._raw_user.get("is_blocked")

    @property
    def is_muted(self) -> bool | None:
        return self._raw_user.get("is_muted")

    @property
    def is_renote_muted(self) -> bool | None:
        return self._raw_user.get("is_renote_muted")

    @property
    def notify(self) -> IUserNotify | None:
        return self._raw_user.get("notify")

    @property
    def with_replies(self) -> bool | None:
        return self._raw_user.get("with_replies")


class MeDetailedOnly:
    def __init__(self, raw_user: IMeDetailedOnlySchema, *, client: ClientManager) -> None:
        self._raw_user: IMeDetailedOnlySchema = raw_user
        self.__client: ClientManager = client

    @property
    def avatar_id(self) -> str | None:
        return self._raw_user["avatar_id"]

    @property
    def banner_id(self) -> str | None:
        return self._raw_user["banner_id"]

    @property
    def is_moderator(self) -> bool | None:
        return self._raw_user["is_moderator"]

    @property
    def is_admin(self) -> bool | None:
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
    def two_factor_backup_codes_stock(self) -> ITwoFactorBackupCodesStock:
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
    def unread_announcements(self) -> list[Announcement]:
        return [
            Announcement(i, client=self.__client) for i in self._raw_user["unread_announcements"]
        ]

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
    def unread_notifications_count(self) -> int:
        return self._raw_user["unread_notifications_count"]

    @property
    def muted_words(self) -> list[list[str]]:
        return self._raw_user["muted_words"]

    @property
    def hard_muted_words(self) -> list[list[str]]:
        return self._raw_user["hard_muted_words"]

    @property
    def muted_instances(self) -> list[str]:
        return self._raw_user["muted_instances"]

    @property
    def notification_recieve_config(self) -> NotificationRecieveConfig:  # TODO: モデル化
        return self._raw_user["notification_recieve_config"]

    @property
    def email_notification_types(self) -> list[EmailNotificationTypes]:  # TODO: モデル化
        return self._raw_user["email_notification_types"]

    @property
    def achievements(self) -> list[Achievement]:
        return [Achievement(i) for i in self._raw_user["achievements"]]

    @property
    def logged_in_days(self) -> int:
        return self._raw_user["logged_in_days"]

    @property
    def policies(self) -> IPolicies:  # TODO: モデル化
        return self._raw_user["policies"]

    @property
    def email(self) -> str | None:
        return self._raw_user.get("email")

    @property
    def email_verified(self) -> bool | None:
        return self._raw_user.get("email_verified")

    @property
    def security_keys_list(self) -> list[IUserSecurityKey] | None:  # TODO: モデル化
        return self._raw_user.get("security_keys_list")


class UserDetailedNotMe[T: IUserDetailedNotMeSchema](PartialUser[T], UserDetailedNotMeOnly):  # pyright: ignore 直せない
    def __init__(self, raw_user: T, *, client: ClientManager) -> None:
        super().__init__(raw_user, client=client)


class MeDetailed(UserDetailedNotMe[IMeDetailedSchema], MeDetailedOnly):  # pyright: ignore 直せない
    def __init__(self, raw_user: IMeDetailedSchema, *, client: ClientManager):
        super().__init__(raw_user, client=client)


def packed_user(user: IUser, client: ClientManager) -> UserDetailedNotMe | MeDetailed:
    if is_user_detailed_not_me(user):
        return UserDetailedNotMe(user, client=client)
    if is_me_detailed(user):
        return MeDetailed(user, client=client)
    raise ValueError("Invalid user model")


class UserList:
    def __init__(self, raw_user_list: IUserList, *, client: ClientManager) -> None:
        self._raw_user_list: IUserList = raw_user_list
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self._raw_user_list["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._raw_user_list["created_at"])

    @property
    def name(self) -> str:
        return self._raw_user_list["name"]

    @property
    def user_ids(self) -> list[str]:
        return self._raw_user_list["user_ids"]

    @property
    def is_public(self) -> bool:
        return self._raw_user_list["is_public"]

    @property
    def api(self) -> ClientUserListManager:
        return self.__client.user._create_client_user_list_manager(self.id)

    def _get(self, key: str) -> Any | None:
        return self._raw_user_list.get(key)


class UserListMembership:
    def __init__(
        self, raw_user_list_membership: IUserListMembership, *, client: ClientManager
    ) -> None:
        self.__raw_user_list_membership: IUserListMembership = raw_user_list_membership
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_user_list_membership["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__raw_user_list_membership["created_at"])

    @property
    def user_id(self) -> str:
        return self.__raw_user_list_membership["user_id"]

    @property
    def user(self) -> PartialUser:
        return PartialUser(self.__raw_user_list_membership["user"], client=self.__client)

    @property
    def with_replies(self) -> bool:
        return self.__raw_user_list_membership["with_replies"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_user_list_membership.get(key)


class FrequentlyRepliedUser:
    def __init__(
        self,
        raw_frequently_replied_user: GetFrequentlyRepliedUsersResponse,
        *,
        client: ClientManager,
    ):
        self._raw_frequently_replied_user: GetFrequentlyRepliedUsersResponse = (
            raw_frequently_replied_user
        )
        self.__client: ClientManager = client

    @property
    def user(self) -> UserDetailedNotMe | MeDetailed:
        return packed_user(self._raw_frequently_replied_user["user"], client=self.__client)

    @property
    def weight(self) -> int:
        return self._raw_frequently_replied_user["weight"]

    def _get(self, key: str) -> Any | None:
        return self._raw_frequently_replied_user.get(key)
