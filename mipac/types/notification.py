"""
WebSocketで来る通知の型を定義しています

NfはNotificationの略です
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mipac.types.note import INote
    from mipac.types.user import ILiteUser


class Notification(TypedDict):
    id: str
    created_at: str
    is_read: bool


class IReactionNf(Notification):
    type: str
    reaction: str
    user: ILiteUser
    user_id: str
    note: INote
