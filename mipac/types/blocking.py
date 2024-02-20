from typing import TypedDict

from mipac.types.user import IUserDetailedNotMeSchema


class IBlocking(TypedDict):
    id: str
    created_at: str
    blockee_id: str
    blockee: IUserDetailedNotMeSchema
