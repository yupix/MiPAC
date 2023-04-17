from typing import NotRequired, TypedDict

from mipac.types.note import IPartialNote


class IPartialChannel(TypedDict):
    id: str
    name: str


class IChannelNote(IPartialNote):
    channel: IPartialChannel
    channel_id: str
    local_only: bool


class IChannelLite(IPartialChannel):
    created_at: str
    last_noted_at: str | None
    description: str | None
    user_id: str
    banner_url: str | None
    users_count: int
    notes_count: int
    pinned_note_ids: NotRequired[list[str]]  # pinned系は 13.11.0以上が必要
    pinned_notes: NotRequired[list[IChannelNote]]


class IChannel(IChannelLite):
    has_unread_note: bool
    is_following: bool | None
    is_favorited: bool | None  # is_favoritedは 13.11.0以上が必要
