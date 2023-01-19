from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mipac.types.user import IUserDetailed


class IModerationLog(TypedDict):
    id: str
    created_at: str
    type: str
    info: dict  # TODO: これ何?
    user_id: str
    user: IUserDetailed
