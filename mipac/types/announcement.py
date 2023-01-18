from typing import TypedDict


class IAnnouncement(TypedDict):
    id: str
    created_at: str
    updated_at: str | None
    text: str
    title: str
    image_url: str | None
    is_read: bool
