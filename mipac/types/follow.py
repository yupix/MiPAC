from typing import TypedDict

from mipac.types.user import ILiteUser


class IFollowRequest(TypedDict):
    id: str
    follower: ILiteUser
    followee: ILiteUser
