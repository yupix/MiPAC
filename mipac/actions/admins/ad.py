from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, override

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
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

    async def delete(self, *, id: str | None = None) -> bool:
        ad_id = self._ad_id or id

        if ad_id is None:
            raise ParameterError("ad id is required")
        res: bool = await self._session.request(
            Route("POST", "/api/admin/ad/delete"), json={"id": ad_id}, auth=True, lower=True
        )
        return res

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


class AdminAdvertisingActions(AdminAdvertisingModelActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        url: str,
        memo: str,
        place: Literal["square", "horizontal", "horizontal-big"],
        priority: Literal["high", "middle", "low"],
        ratio: int,
        expires_at: str,
        starts_at: str,
        image_url: str,
        day_or_week: int,
    ) -> Ad:
        data = {
            "url": url,
            "memo": memo or "",
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "expiresAt": expires_at,
            "startsAt": starts_at,
            "imageUrl": image_url,
            "dayOfWeek": day_or_week,
        }
        raw_ad: IAd = await self._session.request(
            Route("POST", "/api/admin/ad/create"), json=data, auth=True, lower=True
        )
        return Ad(ad_data=raw_ad, client=self._client)

    @override
    async def delete(self, id: str) -> bool:
        return await super().delete(id=id)

    async def get_list(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        publishing: bool | None = None,
    ):
        data = {
            "limit": limit,
            "sinceId": since_id,
            "until_id": until_id,
            "publishing": publishing,
        }

        raw_ads: list[IAd] = await self._session.request(
            Route("POST", "/api/admin/ad/list"), auth=True, json=data
        )

        return [Ad(raw_ad, client=self._client) for raw_ad in raw_ads]

    async def get_all_list(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        publishing: bool | None = None,
    ) -> AsyncGenerator[Ad, None]:
        data = {
            "limit": limit,
            "sinceId": since_id,
            "until_id": until_id,
            "publishing": publishing,
        }

        pagination = Pagination[IAd](
            http_client=self._session, route=Route("POST", "/api/admin/ad/list"), json=data
        )

        while pagination.is_final:
            raw_ads = await pagination.next()

            for raw_ad in raw_ads:
                yield Ad(ad_data=raw_ad, client=self._client)
