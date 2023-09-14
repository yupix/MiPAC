from typing import TypedDict

from mipac.types.user import ILiteUser


class IPartialInviteCode(TypedDict):
    code: str


class IInviteCode(IPartialInviteCode):
    id: str
    expires_at: str | None
    created_at: str
    created_by: str | None
    used_by: ILiteUser | None
    used_at: str | None
    used: bool
