from typing import TypedDict

from mipac.types.user import IPartialUser


class IInviteCode(TypedDict):
    id: str
    code: str
    expires_at: str | None
    created_at: str
    created_by: IPartialUser | None
    used_by: IPartialUser | None
    used_at: str | None
    used: bool


class IInviteLimit(TypedDict):
    remaining: int | None
