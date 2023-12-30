from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.user import BlockingUser, MeDetailed, UserDetailedNotMe, packed_user
from mipac.types.user import IBlockingUser, IUserDetailed
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class BlockingActions(AbstractAction):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def add(self, user_id: str | None = None) -> UserDetailedNotMe | MeDetailed:
        user_id = self.__user_id or user_id
        res: IUserDetailed = await self.__session.request(
            Route("POST", "/api/blocking/create"), auth=True, json={"userId": user_id}, lower=True
        )
        return packed_user(res, client=self.__client)

    async def remove(self, user_id: str | None = None) -> UserDetailedNotMe | MeDetailed:
        user_id = self.__user_id or user_id
        res: IUserDetailed = await self.__session.request(
            Route("POST", "/api/blocking/delete"), auth=True, json={"userId": user_id}, lower=True
        )
        return packed_user(res, client=self.__client)

    async def get_list(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 100,
        get_all: bool = False,
    ) -> AsyncGenerator[BlockingUser, None]:
        if get_all:
            limit = 100

        data = {"limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IBlockingUser](
            self.__session, Route("POST", "/api/blocking/list"), json=data
        )

        while True:
            res_users = await pagination.next()
            for user in res_users:
                yield BlockingUser(user, client=self.__client)
            if get_all is False or pagination.is_final:
                break
