from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, TypeGuard, TypedDict, Any


if TYPE_CHECKING:
    from mipac.types.announcement import IAnnouncement
    from mipac.types.emoji import ICustomEmojiLite
    from mipac.types.instance import IInstanceLite
    from mipac.types.note import INote
    from mipac.types.page import IPage
__all__ = (
    "IFollowRequest",
    "IUserRequired",
    "ILiteUser",
    "IUserDetailed",
    "IUserDetailedField",
    "IAchievement",
    "IBlockingUser",
)


class IBlockingUser(TypedDict):
    id: str
    created_at: str
    blockee_id: str
    blockee: IUserDetailed


class ISignin(TypedDict):
    id: str
    created_at: str
    user_id: str
    ip: str
    headers: dict[str, str]
    success: bool


class IAchievement(TypedDict):
    name: str
    unlocked_at: int


class IBadgeRole(TypedDict):
    name: str
    icon_url: str | None
    display_order: int


class IUserRole(IBadgeRole):
    id: str
    color: str | None
    description: str
    is_moderator: bool
    is_administrator: bool


class IUserRequired(TypedDict):
    id: str
    username: str
    name: str
    online_status: Literal["online", "active", "offline", "unknown"]
    avatar_url: str
    avatar_blurhash: str


class ILiteUser(IUserRequired, total=False):
    host: str
    instance: IInstanceLite
    emojis: list[ICustomEmojiLite]
    avatar_color: str
    badge_roles: list[IBadgeRole]  # v13なら絶対あるはずだけど、他のにはロールそのものが無いので


class IUserDetailedField(TypedDict):
    name: str
    value: str


class IUserDetailedRequired(ILiteUser):
    fields: list[IUserDetailedField]
    followers_count: int
    following_count: int
    has_pending_follow_request_from_you: bool
    has_pending_follow_request_to_you: bool
    is_admin: bool
    is_blocked: bool
    is_blocking: bool
    is_bot: bool
    is_cat: bool
    is_followed: bool
    is_following: bool
    is_locked: bool
    is_moderator: bool
    is_muted: bool
    is_silenced: bool
    is_suspended: bool
    public_reactions: bool
    security_keys: bool
    two_factor_enabled: bool
    notes_count: int
    pinned_note_ids: list[str]
    pinned_notes: List[INote]


class IUserDetailed(IUserDetailedRequired, total=False):
    achievements: List[IAchievement]
    banner_blurhash: str
    banner_color: str
    banner_url: str
    birthday: str
    created_at: str
    description: str
    ff_visibility: Literal["public", "followers", "private"]
    lang: str
    last_fetched_at: str
    location: str
    logged_in_days: int
    pinned_page: IPage
    pinned_page_id: str
    updated_at: str
    uri: str
    url: str
    roles: list[IUserRole]
    memo: str | None
    moderation_note: str  # Noneではなく空の文字列


class IMeDetailed(IUserDetailed):
    avatar_id: str
    banner_id: str
    auto_accept_followed: bool
    always_mark_nsfw: bool
    careful_bot: bool
    email_notification_types: list[str]
    has_pending_received_follow_request: bool
    has_unread_announcement: bool
    has_unread_antenna: bool
    has_unread_mentions: bool
    has_unread_messaging_message: bool
    has_unread_notification: bool
    has_unread_specified_notes: bool
    hide_online_status: bool
    inject_featured_note: bool
    integrations: dict[str, Any]
    is_deleted: bool
    is_explorable: bool
    muted_words: list[list[str]]
    muting_notification_types: list[str]
    no_crawle: bool
    receive_announcement_email: bool
    use_password_less_login: bool
    unread_announcements: list[IAnnouncement]
    two_factor_backup_codes_stock: Literal["full", "partial", "none"]


class IFollowRequest(TypedDict):
    id: str
    follower: ILiteUser
    followee: ILiteUser


def is_me_detailed(user: IUserDetailed | IMeDetailed, me_id: str) -> TypeGuard[IMeDetailed]:
    return user.get("avatar_id") is not None and user.get("id") == me_id
