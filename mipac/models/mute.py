from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.user import UserDetailed
from mipac.types.mute import IMuteUser

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class MuteUser:
    def __init__(self, data: IMuteUser, *, client: ClientActions) -> None:
        self.__data: IMuteUser = data
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__data['id']

    @property
    def created_at(self) -> str:
        return self.__data['created_at']

    @property
    def mutee_id(self) -> str:
        return self.__data['mutee_id']

    @property
    def mutee(self) -> UserDetailed:
        return UserDetailed(self.__data['mutee'], client=self.__client)
