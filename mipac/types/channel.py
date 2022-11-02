from typing import TypedDict


class IChannel(TypedDict):
    id: str
    created_at: str
    last_noted_at: str
    name: str
    description: str | None
    banner_url: str | None
    notes_count: int
    users_count: int
    is_following: bool
    user_id: str
    has_unread_note: bool
