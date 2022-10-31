from typing import TypedDict

from mipac.types.user import IUserLite


class IFollowRequest(TypedDict):
    id: str
    follower: IUserLite
    followee: IUserLite
