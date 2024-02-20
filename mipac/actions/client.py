from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, overload

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement
from mipac.models.lite.meta import PartialMeta
from mipac.models.meta import Meta
from mipac.types.announcement import IAnnouncement
from mipac.types.meta import IMeta, IPartialMeta
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager) -> None:
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @overload
    async def get_meta(self, detail: Literal[False] = ...) -> PartialMeta:
        ...

    @overload
    async def get_meta(self, detail: Literal[True] = ...) -> Meta:
        ...

    async def get_meta(self, detail: bool = False):
        params = {
            "route": Route("POST", "/api/meta"),
            "json": {"detail": detail},
            "auth": True,
            "lower": True,
        }
        if detail is True:
            meta: IMeta = await self.__session.request(**params)
            return Meta(meta, client=self.__client)
        lite_meta: IPartialMeta = await self.__session.request(**params)
        return PartialMeta(lite_meta, client=self.__client)

    async def get_announcements(
        self,
        limit: int = 10,
        with_unreads: bool = False,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[Announcement, None]:
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")
        if get_all:
            limit = 100

        body = {
            "limit": limit,
            "withUnreads": with_unreads,
            "sinceId": since_id,
            "untilId": until_id,
        }

        pagination = Pagination[IAnnouncement](
            self.__session, Route("POST", "/api/announcements"), json=body
        )

        while True:
            res_announcements = await pagination.next()
            for announcement in res_announcements:
                yield Announcement(announcement, client=self.__client)

            if get_all is False or pagination.is_final:
                break
