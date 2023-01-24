from typing import TypedDict

from mipac.types.user import ILiteUser, IUserDetailed


class IFederationFollowCommon(TypedDict):
    id: str
    created_at: str
    followee_id: str
    followee: IUserDetailed
    follower_id: str
    follower: IUserDetailed


class IFederationFollower(IFederationFollowCommon):
    ...


class IFederationFollowing(IFederationFollowCommon):
    ...


class IFollowRequest(TypedDict):
    id: str
    follower: ILiteUser
    followee: ILiteUser
