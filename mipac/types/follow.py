from typing import NotRequired, TypedDict

from mipac.types.user import IPartialUser, IUserDetailedNotMeSchema


class IFederationFollowCommon(TypedDict):
    id: str
    created_at: str
    followee_id: str
    followee: NotRequired[IUserDetailedNotMeSchema]
    follower_id: str
    follower: NotRequired[IUserDetailedNotMeSchema]


class IFederationFollower(IFederationFollowCommon):
    ...


class IFederationFollowing(IFederationFollowCommon):
    ...


class IFollowRequest(TypedDict):
    id: str
    follower: IPartialUser
    followee: IPartialUser
