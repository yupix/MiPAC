from typing import TypedDict


class IAnnouncementCommon(TypedDict):
    id: str
    created_at: str
    updated_at: str | None
    text: str
    title: str
    image_url: str | None


class IAnnouncement(IAnnouncementCommon):
    """ユーザーから見たアナウンスの状態"""

    is_read: bool


class IAnnouncementSystem(IAnnouncementCommon):
    """システムから見たアナウンスの状態"""

    reads: int
