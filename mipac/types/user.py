from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, TypedDict

if TYPE_CHECKING:
    from mipac.types.channel import IChannel
    from mipac.types.emoji import ICustomEmojiLite
    from mipac.types.instance import IInstanceLite
    from mipac.types.note import INote
    from mipac.types.page import IPage
__all__ = (
    'IUserRequired',
    'IChannel',
    'ILiteUser',
    'IUserDetailed',
    'IUserDetailedField',
)


class ISignin(TypedDict):
    id: str
    created_at: str
    user_id: str
    ip: str
    headers: dict[str, str]
    success: bool


class IUserRequired(TypedDict):
    id: str
    username: str
    name: str
    online_status: Literal['online', 'active', 'offline', 'unknown']
    avatar_url: str
    avatar_blurhash: str
    emojis: list[ICustomEmojiLite]


class ILiteUser(IUserRequired, total=False):
    host: str
    instance: IInstanceLite


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
    banner_blurhash: str
    banner_color: str
    banner_url: str
    birthday: str
    created_at: str
    description: str
    ff_visibility: Literal['public', 'followers', 'private']
    lang: str
    last_fetched_at: str
    location: str
    pinned_page: IPage
    pinned_page_id: str
    updated_at: str
    uri: str
    url: str


class IFollowRequest(TypedDict):
    id: str
    follower: ILiteUser
    followee: ILiteUser
