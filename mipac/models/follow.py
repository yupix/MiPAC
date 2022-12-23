from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.lite.user import LiteUser
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class FollowRequest:
    def __init__(
        self, follow_request: IFollowRequest, *, client: ClientActions
    ) -> None:
        self.__follow_request = follow_request
        self.__client = client

    @property
    def id(self) -> str:
        return self.__follow_request['id']

    @property
    def follower(self) -> LiteUser:
        return LiteUser(
            self.__follow_request['follower'], client=self.__client
        )

    @property
    def followee(self) -> LiteUser:
        return LiteUser(
            self.__follow_request['followee'], client=self.__client
        )
