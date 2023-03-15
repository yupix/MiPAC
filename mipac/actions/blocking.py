from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.user import BlockingUser, UserDetailed
from mipac.types.user import IBlockingUser, IUserDetailed

if TYPE_CHECKING:
    from mipac.client import ClientManager


class BlockingActions(AbstractAction):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def add(self, user_id: str | None = None) -> UserDetailed:
        user_id = self.__user_id or user_id
        res: IUserDetailed = await self.__session.request(
            Route('POST', '/api/blocking/create'), auth=True, json={'userId': user_id}, lower=True
        )
        return UserDetailed(res, client=self.__client)

    async def remove(self, user_id: str | None = None) -> UserDetailed:
        user_id = self.__user_id or user_id
        res: IUserDetailed = await self.__session.request(
            Route('POST', '/api/blocking/delete'), auth=True, json={'userId': user_id}, lower=True
        )
        return UserDetailed(res, client=self.__client)

    async def get_list(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 100,
        all: bool = False,
    ) -> AsyncGenerator[BlockingUser, None]:
        async def request(body) -> list[BlockingUser]:
            res: list[IBlockingUser] = await self.__session.request(
                Route('POST', '/api/blocking/list'), lower=True, auth=True, json=body
            )
            return [BlockingUser(user, client=self.__client) for user in res]

        data = {'limit': limit, 'sinceId': since_id, 'untilId': until_id}
        if all:
            data['limit'] = 100
        first_req = await request(data)
        for user in first_req:
            yield user

        if all and len(first_req) == 100:
            data['untilId'] = first_req[-1].id
            while True:
                res = await request(data)
                if len(res) <= 100:
                    for user in res:
                        yield user
                if len(res) == 0:
                    break
                data['untilId'] = res[-1].id
