from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.blocking import Blocking
from mipac.models.user import MeDetailed, UserDetailedNotMe, packed_user
from mipac.types.blocking import IBlocking
from mipac.types.user import IUserDetailed
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedBlockingActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def add(self, *, user_id: str) -> UserDetailedNotMe | MeDetailed:
        res: IUserDetailed = await self._session.request(
            Route("POST", "/api/blocking/create"), auth=True, json={"userId": user_id}, lower=True
        )
        return packed_user(res, client=self._client)

    async def remove(self, *, user_id: str) -> UserDetailedNotMe | MeDetailed:
        res: IUserDetailed = await self._session.request(
            Route("POST", "/api/blocking/delete"), auth=True, json={"userId": user_id}, lower=True
        )
        return packed_user(res, client=self._client)


class ClientBlockingActions(SharedBlockingActions):
    """クライアント用のブロックアクション

    基本的にoverride以外は行わない
    """

    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user_id: str = user_id

    @override
    async def add(self, *, user_id: str | None = None) -> UserDetailedNotMe | MeDetailed:
        user_id = user_id or self.__user_id
        return await super().add(user_id=user_id)

    @override
    async def remove(self, *, user_id: str | None = None) -> UserDetailedNotMe | MeDetailed:
        user_id = user_id or self.__user_id
        return await super().remove(user_id=user_id)


class BlockingActions(SharedBlockingActions):
    """ブロックアクション
    user_idを持たないメソッドのみを持ち、持つものはSharedBlockingActionsに実装する
    """

    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def get_list(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 100,
    ) -> list[Blocking]:
        body = {"limit": limit, "sinceId": since_id, "untilId": until_id}
        raw_blocking_list = await self._session.request(
            Route("POST", "/api/blocking/list"), json=body, auth=True
        )
        return [
            Blocking(raw_blocking=blocking, client=self._client) for blocking in raw_blocking_list
        ]

    async def get_all_list(
        self, limit: int = 30, since_id: str | None = None, until_id: str | None = None
    ) -> AsyncGenerator[Blocking, None]:
        pagination = Pagination[IBlocking](
            self._session,
            Route("POST", "/api/blocking/list"),
            json={"limit": limit, "sinceId": since_id, "untilId": until_id},
        )

        while pagination.is_final is False:
            raw_blocking = await pagination.next()
            for raw_blocking in raw_blocking:
                yield Blocking(raw_blocking=raw_blocking, client=self._client)
