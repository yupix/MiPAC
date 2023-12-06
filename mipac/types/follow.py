from typing import NotRequired, TypedDict

from mipac.types.user import IPartialUser, IUserDetailed


class IFederationFollowCommon(TypedDict):
    id: str
    created_at: str
    followee_id: str
    followee: NotRequired[IUserDetailed]
    follower_id: str
    follower: NotRequired[IUserDetailed]


class IFederationFollower(IFederationFollowCommon):
    ...


class IFederationFollowing(IFederationFollowCommon):
    ...


class IFollowRequest(TypedDict):
    id: str
    follower: IPartialUser
    followee: IPartialUser
