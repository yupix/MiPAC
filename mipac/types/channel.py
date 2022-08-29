from typing import TypedDict


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
