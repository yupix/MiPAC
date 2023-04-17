from typing import TypedDict


class IChannelLite(TypedDict):
    id: str
    created_at: str
    last_noted_at: str | None
    name: str
    description: str | None
    user_id: str
    banner_url: str | None
    users_count: int
    notes_count: int
    pinned_note_ids: list | None  # pinned系は 13.11.0以上が必要
    pinned_notes: list | None  


class IChannel(IChannelLite):
    has_unread_note: bool
    is_following: bool | None
    is_favorited: bool | None  # is_favoritedは 13.11.0以上が必要
