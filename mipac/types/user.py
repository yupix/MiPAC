from __future__ import annotations

from typing import Any, List, Literal, Optional, TypedDict

from .drive import IDriveFile
from .emoji import EmojiPayload, ICustomEmojiLite
from .instance import IInstanceLite, InstancePayload

__all__ = (
    'IChannel',
    'FieldContentPayload',
    'UserPayload',
    'PinnedPagePayload',
    'IPinnedNote',
    'OptionalUser',
)


class IUserLite(TypedDict):
    id: str
    username: str
    host: str | None
    name: str
    online_status: Literal['online', 'active', 'offline', 'unknown']
    avatar_url: str
    avatar_blurhash: str
    emojis: list[ICustomEmojiLite]
    instance: IInstanceLite


class IChannel(TypedDict, total=False):
    id: str
    created_at: str
    last_noted_at: str
    name: str
    description: str
    banner_url: str
    notes_count: int
    users_count: int
    is_following: bool
    user_id: str


class IPinnedNote(TypedDict, total=False):
    id: str
    created_at: str
    text: str
    cw: str
    user_id: str
    user: 'UserPayload'
    reply_id: str
    renote_id: str
    reply: dict[str, Any]
    renote: dict[str, Any]
    via_mobile: bool
    is_hidden: bool
    visibility: str
    mentions: list[str]
    visible_user_ids: list[str]
    file_ids: list[str]
    files: list[IDriveFile]
    tags: list[str]
    poll: dict[str, Any]
    channel_id: str
    channel: IChannel
    local_only: bool
    emojis: list[EmojiPayload]
    reactions: dict[str, Any]
    renote_count: int
    replies_count: int
    uri: str
    url: str
    my_reaction: dict[str, Any]


class PinnedPagePayload(TypedDict):
    id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    title: Optional[str]
    name: Optional[str]
    summary: Optional[str]
    content: Optional[List]
    variables: Optional[List]
    user_id: Optional[str]
    author: Optional[dict[str, Any]]


class FieldContentPayload(TypedDict):
    name: str
    value: str


class OptionalUser(TypedDict, total=False):
    user_id: str
    name: str
    host: str
    is_admin: bool
    is_moderator: bool
    is_bot: bool
    is_cat: bool
    is_lady: bool
    online_status: str


class UserPayload(OptionalUser):
    id: str
    username: str
    avatar_url: Optional[str]
    avatar_blurhash: Optional[str]
    avatar_color: Optional[str]
    emojis: Optional[list[str]]
    url: str
    uri: str
    created_at: str
    updated_at: str
    is_locked: bool
    is_silenced: bool
    is_suspended: bool
    description: str
    location: str
    birthday: str
    fields: Any
    followers_count: int
    following_count: int
    notes_count: int
    pinned_note_ids: list[str]
    pinned_notes: list[str]
    pinned_page_id: str
    pinned_page: str
    ff_visibility: str
    is_following: bool
    is_follow: bool
    is_blocking: bool
    is_blocked: bool
    is_muted: bool
    instance: Optional[InstancePayload]
