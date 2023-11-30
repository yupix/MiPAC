from typing import TypedDict

from mipac.types.user import IPartialUser


class IPartialInviteCode(TypedDict):
    code: str


class IInviteCode(IPartialInviteCode):
    id: str
    expires_at: str | None
    created_at: str
    created_by: IPartialUser | None
    used_by: IPartialUser | None
    used_at: str | None
    used: bool
