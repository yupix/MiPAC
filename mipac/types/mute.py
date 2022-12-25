from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mipac.types.user import IUserDetailed


class IMuteUser(TypedDict):
    id: str
    created_at: str
    mutee_id: str
    mutee: IUserDetailed
