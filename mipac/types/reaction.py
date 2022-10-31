from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from mipac.types.user import IUserLite

__all__ = ('NoteReactionPayload',)


class NoteReactionPayload(TypedDict):
    id: str
    created_at: str
    user: IUserLite
    type: str
