"""
WebSocketで来る通知の型を定義しています

NfはNotificationの略です
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mipac.types.note import INote
    from mipac.types.user import ILiteUser


class INotification(TypedDict):
    id: str
    type: str
    created_at: str
    is_read: bool


class IUserNf(INotification):
    user: ILiteUser
    user_id: str


class INoteNf(INotification):
    user: ILiteUser
    user_id: str
    note: INote


class IPollEndNf(INotification):
    note: INote


class IReactionNf(INotification):
    reaction: str
    user: ILiteUser
    user_id: str
    note: INote
