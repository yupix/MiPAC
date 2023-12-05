from typing import NotRequired, TypedDict


class IAnnouncement(TypedDict):
    id: str
    createdAt: str
    updatedAt: str | None
    text: str
    title: str
    imageUrl: str | None
    icon: str | None
    display: str
    needConfirmationToRead: bool
    silence: bool
    forYou: bool
    isRead: NotRequired[bool]


class IAnnouncementDetailed(TypedDict):
    """管理者から見たアナウンス"""

    id: str
    created_at: str
    updated_at: str | None
    title: str
    text: str
    image_url: str | None
    icon: str | None
    display: str
    is_active: bool
    for_existing_users: bool
    silence: bool
    need_confirmation_to_read: bool
    user_id: str | None
    reads: int
