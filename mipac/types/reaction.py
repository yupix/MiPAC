from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from mipac.types.user import IPartialUser

__all__ = ("NoteReactionPayload",)

IReactionAcceptance = Literal["likeOnly", "likeOnlyForRemote"]


class NoteReactionPayload(TypedDict):
    id: str
    created_at: str
    user: IPartialUser
    type: str
