from __future__ import annotations

from typing import TYPE_CHECKING, List, TypedDict

if TYPE_CHECKING:
    from mipac.types import IDriveFile
    from mipac.types.user import ILiteUser

__all__ = ('IChatGroup', 'IChatMessage')


class IChatGroup(TypedDict):
    id: str
    created_at: str
    name: str
    owner_id: str
    user_ids: list[str]


class IChatMessage(TypedDict):
    id: str
    created_at: str
    file: IDriveFile
    text: str | None
    user_id: str
    user: ILiteUser
    recipient_id: str
    recipient: str
    group_id: str
    file_id: str
    is_read: list[str]
    reads: List
    group: IChatGroup | None
