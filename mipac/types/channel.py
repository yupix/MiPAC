from typing import NotRequired, TypedDict

from mipac.types.note import INote


class IChannel(TypedDict):
    id: str
    created_at: str
    last_noted_at: str | None
    name: str
    description: str | None
    user_id: str | None
    banner_url: str | None
    pinned_note_ids: list[str]
    color: str
    is_archived: bool
    users_count: int
    notes_count: int
    is_sensitive: bool
    allow_renote_to_external: bool
    is_following: NotRequired[bool]
    is_favorited: NotRequired[bool]
    pinned_notes: NotRequired[list[INote]]
