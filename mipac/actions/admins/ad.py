from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion, NotSupportVersionText, ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.ad import Ad
from mipac.types.ads import IAd
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminAdvertisingModelActions(AbstractAction):
    def __init__(self, ad_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self._ad_id: str | None = ad_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def update(
        self,
        url: str,
        place: Literal["square", "horizontal", "horizontal-big"],
        priority: Literal["high", "middle", "low"],
        ratio: int,
        image_url: str,
        id: str | None = None,
        starts_at: int = 0,
        expires_at: int = 0,
        memo: str | None = None,
    ) -> bool:
        ad_id = self._ad_id or id
        if ad_id is None:
            raise ParameterError("ad_idは必須です")
        data = {
            "id": ad_id,
            "url": url,
            "memo": memo or "",
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "startsAt": starts_at,
            "expiresAt": expires_at,
            "imageUrl": image_url,
        }
        res: bool = await self._session.request(
            Route("POST", "/api/admin/ad/update"), json=data, auth=True, lower=True
        )
        return res

    async def delete(self, id: str | None = None) -> bool:
        ad_id = self._ad_id or id
        res: bool = await self._session.request(
            Route("POST", "/api/admin/ad/delete"), json={"id": ad_id}, auth=True, lower=True
        )
        return res


class AdminAdvertisingActions(AdminAdvertisingModelActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        url: str,
        place: Literal["square", "horizontal", "horizontal-big"],
        priority: Literal["high", "middle", "low"],
        ratio: int,
        image_url: str,
        starts_at: int = 0,
        expires_at: int = 0,
        memo: str | None = None,
    ) -> bool:
        data = {
            "url": url,
            "memo": memo or "",
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "startsAt": starts_at,
            "expiresAt": expires_at,
            "imageUrl": image_url,
        }
        res: bool = await self._session.request(
            Route("POST", "/api/admin/ad/create"), json=data, auth=True, lower=True
        )
        return res

    async def get_list(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[Ad, None]:
        if limit > 100:
            raise ParameterError("limitは100以下である必要があります")

        if get_all:
            limit = 100

        data = {"limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IAd](self._session, Route("POST", "/api/admin/ad/list"), json=data)

        while True:
            raw_ads = await pagination.next()
            for raw_ad in raw_ads:
                yield Ad(raw_ad, client=self._client)

            if get_all is False or pagination.is_final:
                break
