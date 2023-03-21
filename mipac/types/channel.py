from typing import TypedDict


class IChannelLite(TypedDict):
    id: str
    created_at: str
    last_noted_at: str | None
    name: str
    description: str | None
    banner_url: str | None
    notes_count: int
    users_count: int
    is_following: bool
    user_id: str

class IChannel(IChannelLite):
    has_unread_note: bool
