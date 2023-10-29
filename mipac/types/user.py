from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict, TypeGuard

from mipac.types.roles import IPartialRole

if TYPE_CHECKING:
    from mipac.types.announcement import IAnnouncement
    from mipac.types.instance import IInstanceLite
    from mipac.types.note import INote
    from mipac.types.page import IPage

IUserOnlineStatus = Literal["online", "active", "offline", "unknown"]
IFfVisibility = Literal["public", "followers", "private"]
IUserNotify = Literal["normal", "none"]


class IUserField(TypedDict):
    name: str
    value: str


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


class IPartialUser(TypedDict):
    id: str
    name: str | None
    username: str
    host: str | None
    avatar_url: str
    avatar_blurhash: str
    is_bot: bool
    is_cat: bool
    instance: NotRequired[IInstanceLite]  # ローカルユーザーの場合はキーが無い
    emojis: dict[str, str]
    online_status: IUserOnlineStatus
    badge_roles: NotRequired[list[IBadgeRole]]  # リモートユーザーの場合はキーが無い


class IUserDetailedNotLogined(IPartialUser):
    """
    ログイン無し
    """

    url: str | None  # ローカルユーザーには無い
    uri: str | None  # # ローカルユーザーには無い
    moved_to: str | None  # ユーザーのID
    also_known_as: list[str] | None
    created_at: str
    updated_at: str | None
    last_fetched_at: str | None  # ローカルユーザーには無い
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
    ff_visibility: IFfVisibility
    two_factor_enabled: bool
    use_password_less_login: bool
    security_keys: bool
    roles: list[IPartialRole]
    memo: str | None


class IUserDetailed(IUserDetailedNotLogined):
    """
    主に自分から見た相手の情報が追加される
    ログイン済み
    モデレーターではない
    """

    is_following: bool
    is_followed: bool
    has_pending_follow_request_from_you: bool
    has_pending_follow_request_to_you: bool
    is_blocking: bool
    is_blocked: bool
    is_muted: bool
    is_renote_muted: bool
    notify: IUserNotify


class IUserDetailedModerator(IUserDetailed):
    """モデレーターから見たユーザー"""

    moderation_note: str


class IMeDetailed(IUserDetailed):
    """自分自身"""

    avatar_id: str
    banner_id: None
    is_moderator: bool
    is_admin: bool
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
    two_factor_backup_codes_stock: str
    hide_online_status: bool
    has_unread_specified_notes: bool
    has_unread_mentions: bool
    has_unread_announcement: bool
    unread_announcements: IAnnouncement
    has_unread_antenna: bool
    has_unread_channel: bool
    has_unread_notification: bool
    has_pending_received_follow_request: bool
    muted_words: list[str]
    muted_instances: dict
    muting_notification_types: dict
    notification_recieve_config: dict
    email_notification_types: dict
    achievements: dict
    logged_in_days: int
    policies: dict


class IMeDetailedModerator(IMeDetailed):
    """自分自身でモデレーター"""

    moderation_note: str


# 型が不明確になるため、基本的にはこの共用体は使わないでください。基本的にAPIなどのレスポンスに使うことを想定しています。
IUser = (
    IPartialUser
    | IUserDetailedNotLogined
    | IUserDetailed
    | IUserDetailedModerator
    | IMeDetailed
    | IMeDetailedModerator
)


class IFollowRequest(TypedDict):
    id: str
    follower: IPartialUser
    followee: IPartialUser


def is_partial_user(user: IUser) -> TypeGuard[IPartialUser]:
    return user.get("created_at") is None


def is_me_detailed(user: IUser, me_id: str) -> TypeGuard[IMeDetailed]:
    return user.get("avatar_id") is not None and user.get("id") == me_id


def is_user_detailed_not_logined(user: IUser) -> TypeGuard[IUserDetailedNotLogined]:
    """
    渡されたユーザーがログイン無しで取得された情報か確認します。またこれは自分自身ではないです。

    Parameters
    ----------
    user : IUser
        user information

    Returns
    -------
    TypeGuard[IUserDetailedNotLogined]
    """
    return (
        user.get("is_following", "d3ee116d-1ee7-4a35-b277-0e22d541912e")
        == "d3ee116d-1ee7-4a35-b277-0e22d541912e"
    )


def is_user_detailed(user: IUser) -> TypeGuard[IUserDetailed]:
    """
    渡されたユーザーがログイン済みで自分自身ではないかを判定します

    Parameters
    ----------
    user : IUser
        user information

    Returns
    -------
    TypeGuard[IUserDetailed]
    """

    return (
        user.get("avatar_id", "61a0dc68-bf6f-4947-9e9a-348db9c7de08")
        == "61a0dc68-bf6f-4947-9e9a-348db9c7de08"
    )


def is_user_detailed_moderator(user: IUser) -> TypeGuard[IUserDetailedModerator]:
    """
    渡されたユーザーがモデレーターから見たユーザーかを判定します

    Parameters
    ----------
    user : IUser
        user information

    Returns
    -------
    TypeGuard[IUserDetailedModerator]
    """

    return user.get("moderation_note") is not None


def is_me_detailed_moderator(user: IUser, me_id: str) -> TypeGuard[IMeDetailedModerator]:
    """
    渡されたユーザーが自分自身克モデレーターかを判定します

    Parameters
    ----------
    user : IUser
        user information

    Returns
    -------
    TypeGuard[IMeDetailedModerator]
    """

    return user.get("moderation_note") is not None and user.get("id") == me_id
