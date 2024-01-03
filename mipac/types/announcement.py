from typing import NotRequired, TypedDict


class IAnnouncement(TypedDict):
    id: str
    created_at: str
    updated_at: str | None
    text: str
    title: str
    image_url: str | None
    icon: str
    display: str
    need_confirmation_to_read: bool
    silence: bool
    for_you: bool
    is_read: NotRequired[bool]


class IAnnouncementDetailed(TypedDict):
    """管理者から見たアナウンス"""

    id: str
    created_at: str
    updated_at: str | None
    text: str
    title: str
    image_url: str | None
    icon: str
    display: str
    need_confirmation_to_read: bool
    silence: bool

    is_active: bool
    for_existing_users: bool
    user_id: str | None
    reads: int
