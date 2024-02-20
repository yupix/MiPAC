from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict, TypeGuard

from mipac.types.meta import IPolicies
from mipac.types.roles import IPartialRole

if TYPE_CHECKING:
    from mipac.types.announcement import IAnnouncement
    from mipac.types.instance import IInstanceLite
    from mipac.types.note import INote
    from mipac.types.page import IPage

IUserOnlineStatus = Literal["online", "active", "offline", "unknown"]
IFfVisibility = Literal["public", "followers", "private"]
IUserNotify = Literal["normal", "none"]
ITwoFactorBackupCodesStock = Literal["full", "partial", "none"]
NotificationRecieveConfigOption = Literal[
    "all", "following", "follower", "mutualFollow", "never"
]  # Misskey側が間違っている(Receiveのミススペル?)ので混乱を招かないようにこっちも統一してある
EmailNotificationTypes = Literal["mention", "reply", "quote", "follow", "receiveFollowRequest"]


class IUserField(TypedDict):
    name: str
    value: str


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
    """
    Deprecated

    Will be removed in v0.7.0
    """

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


class IAvatarDecoration(TypedDict):
    id: str
    angle: NotRequired[int]
    flip_h: NotRequired[bool]
    url: str
    offset_x: NotRequired[int]
    offset_y: NotRequired[int]


class NotificationRecieveConfigType(TypedDict):
    type: NotificationRecieveConfigOption


class NotificationRecieveConfigWithUserList(TypedDict):
    type: NotificationRecieveConfigOption
    user_list_id: str


class NotificationRecieveConfig(TypedDict):
    note: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    follow: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    mention: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    reply: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    renote: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    quote: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    reaction: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    pollEnded: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    receive_follow_request: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    follow_request_accepted: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    role_assigned: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    achievement_earned: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    app: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList
    test: NotificationRecieveConfigType | NotificationRecieveConfigWithUserList


class IUserSecurityKey(TypedDict):
    id: str
    name: str
    last_used: str


class IPartialUser(TypedDict):
    """
    Misskey Schema: `packedUserLiteSchema`
    """

    id: str
    name: str | None
    username: str
    host: str | None
    avatar_url: str | None
    avatar_blurhash: str | None
    avatar_decorations: list[IAvatarDecoration]
    is_bot: NotRequired[bool]
    is_cat: NotRequired[bool]
    instance: NotRequired[IInstanceLite]  # ローカルユーザーの場合はキーが無い
    emojis: dict[str, str]
    online_status: IUserOnlineStatus
    badge_roles: NotRequired[list[IBadgeRole]]  # リモートユーザーの場合はキーが無い


class IUserDetailedNotMeOnlySchema(TypedDict):
    """
    Misskey Schema: `packedUserDetailedNotMeOnlySchema`
    """

    url: str | None
    uri: str | None
    moved_to: str | None
    also_known_as: list[str] | None
    created_at: str
    updated_at: str | None
    last_fetched_at: str | None
    banner_url: str | None
    banner_blurhash: str | None
    is_locked: bool
    is_silenced: bool
    is_suspended: bool
    description: str | None
    location: str | None
    birthday: str | None
    lang: str | None
    fields: list[IUserField]
    verified_links: list[str]
    followers_count: int
    following_count: int
    notes_count: int
    pinned_note_ids: list[str]
    pinned_notes: list[INote]
    pinned_page_id: str | None
    pinned_page: IPage | None  # TODO: IPageが正しいか確認する
    public_reactions: bool
    following_visibility: IFfVisibility
    followers_visibility: IFfVisibility
    two_factor_enabled: bool
    use_password_less_login: bool
    security_keys: bool
    roles: list[IPartialRole]
    memo: str | None
    moderation_note: NotRequired[str]
    is_following: NotRequired[bool]
    is_followed: NotRequired[bool]
    has_pending_follow_request_from_you: NotRequired[bool]
    has_pending_follow_request_to_you: NotRequired[bool]
    is_blocking: NotRequired[bool]
    is_blocked: NotRequired[bool]
    is_muted: NotRequired[bool]
    is_renote_muted: NotRequired[bool]
    notify: NotRequired[IUserNotify]
    with_replies: NotRequired[bool]


class IMeDetailedOnlySchema(TypedDict):
    avatar_id: str | None
    banner_id: str | None
    is_moderator: bool | None  # entities/UserEntityService.ts で roleServiceを用いて判断してるからNoneの場合がある?
    is_admin: bool | None
    inject_featured_note: bool
    receive_announcement_email: bool
    always_mark_nsfw: bool
    auto_sensitive: bool
    careful_bot: bool
    auto_accept_followed: bool
    no_crawle: bool
    prevent_ai_learning: bool
    is_explorable: bool
    is_deleted: bool
    two_factor_backup_codes_stock: ITwoFactorBackupCodesStock
    hide_online_status: bool
    has_unread_specified_notes: bool
    has_unread_mentions: bool
    has_unread_announcement: bool
    unread_announcements: list[IAnnouncement]
    has_unread_antenna: bool
    has_unread_channel: bool
    has_unread_notification: bool
    has_pending_received_follow_request: bool
    unread_notifications_count: bool
    muted_words: list[list[str]]
    hard_muted_words: list[list[str]]
    muted_instances: list[str]
    notification_recieve_config: NotificationRecieveConfig
    email_notification_types: list[EmailNotificationTypes]
    achievements: list[IAchievement]
    logged_in_days: int
    policies: IPolicies
    email: NotRequired[str | None]
    email_verified: NotRequired[bool]
    security_keys_list: NotRequired[list[IUserSecurityKey]]  # セキュリティー


class IUserList(TypedDict):
    id: str
    created_at: str
    name: str
    user_ids: list[str]
    is_public: bool


class IUserListMembership(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: IPartialUser
    with_replies: bool


class IUserDetailedNotMeSchema(IPartialUser, IUserDetailedNotMeOnlySchema):
    pass


class IMeDetailedSchema(IUserDetailedNotMeSchema, IMeDetailedOnlySchema):
    pass


IUserDetailed = IUserDetailedNotMeSchema | IMeDetailedSchema

IUser = IPartialUser | IUserDetailed | IUserDetailedNotMeSchema


def is_partial_user(user: IUser) -> TypeGuard[IPartialUser]:
    """
    他のUser型は全て IUserDetailedNotMeSchema 経由で IUserDetailedNotMeOnlySchema を継承しているため
    url が無いことを確認し区別する
    念のために avatar_url があることも確認する
    """
    if "url" not in user and "avatar_url" in user:
        return True
    return False


def is_user_detailed_not_me(user: IUser) -> TypeGuard[IUserDetailedNotMeSchema]:
    """

    IUserDetailedNotMeSchemaが持つ url が有ることを確認し
    IMeDetailedOnlySchema が持つ avatar_id が無いことを確認する
    こうすることで IMeDetailedSchema と区別する
    """
    if "avatar_id" not in user and "url" in user:
        return True
    return False


def is_me_detailed(user: IUser) -> TypeGuard[IMeDetailedSchema]:
    """
    IMeDetailedOnlySchemaで avatar_id
    IUserDetailedNotMeOnlySchemaで url
    を持っているのでどちらともを満たしたものがIMeDetailedSchema
    """
    if "avatar_id" in user and "url" in user:
        return True
    return False


def is_user_detailed(user: IUser) -> TypeGuard[IUserDetailed]:
    if is_user_detailed_not_me(user) or is_me_detailed(user):
        return True
    return False


####
##  ここからモデルというよりレスポンス
####


class GetFrequentlyRepliedUsersResponse(TypedDict):
    """`users/get-frequently-replied-users` のレスポンス"""

    user: IUserDetailed
    weight: int
