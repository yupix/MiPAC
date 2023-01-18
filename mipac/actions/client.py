from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    AsyncGenerator,
    Literal,
    overload,
)

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement
from mipac.models.lite.meta import LiteMeta
from mipac.models.meta import Meta
from mipac.types.announcement import IAnnouncement
from mipac.types.meta import ILiteMeta, IMeta

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager) -> None:
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @overload
    async def get_meta(self, detail: Literal[False] = ...) -> LiteMeta:
        ...

    @overload
    async def get_meta(self, detail: Literal[True] = ...) -> Meta:
        ...

    async def get_meta(self, detail: bool = False):
        params = {
            'route': Route('POST', '/api/meta'),
            'json': {'detail': detail},
            'auth': True,
            'lower': True,
        }
        if detail is True:
            meta: IMeta = await self.__session.request(**params)
            return Meta(meta, client=self.__client)
        lite_meta: ILiteMeta = await self.__session.request(**params)
        return LiteMeta(lite_meta, client=self.__client)

    async def get_announcements(
        self,
        limit: int = 10,
        with_unreads: bool = False,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        all: bool = False
    ) -> AsyncGenerator[Announcement, None]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if all:
            limit = 100

        async def request(req_body) -> list[Announcement]:
            res: list[IAnnouncement] = await self.__session.request(
                Route('POST', '/api/announcements'), auth=True, json=req_body,
            )
            return [
                Announcement(announcement, client=self.__client)
                for announcement in res
            ]

        body = {
            'limit': limit,
            'withUnreads': with_unreads,
            'sinceId': since_id,
            'untilId': until_id,
        }
        first_req = await request(body)

        for announcement in first_req:
            yield announcement
        if all and len(first_req) == 100:
            body['untilId'] = first_req[-1].id
            count = 0
            while True:
                count = count + 1
                res = await request(body)
                if len(res) <= 100:
                    for announcement in res:
                        yield announcement
                if len(res) < 100:
                    break
