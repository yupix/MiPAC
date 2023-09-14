from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.model import AbstractModel
from mipac.models.lite.user import LiteUser
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.follow import FollowRequestManager


class FollowRequest(AbstractModel):
    def __init__(self, follow_request: IFollowRequest, *, client: ClientManager) -> None:
        self.__follow_request = follow_request
        self.__client = client

    @property
    def id(self) -> str:
        return self.__follow_request["id"]

    @property
    def follower(self) -> LiteUser:
        return LiteUser(self.__follow_request["follower"], client=self.__client)

    @property
    def followee(self) -> LiteUser:
        return LiteUser(self.__follow_request["followee"], client=self.__client)

    @property
    def api(self) -> FollowRequestManager:
        return self.__client._create_user_instance(user=self.follower).follow.request

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, FollowRequest) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
