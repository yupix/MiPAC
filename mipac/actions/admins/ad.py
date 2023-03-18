from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion, NotSupportVersionText, ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.ad import Ad
from mipac.types.ads import IAd

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
        place: Literal['square', 'horizontal', 'horizontal-big'],
        priority: Literal['high', 'middle', 'low'],
        ratio: int,
        image_url: str,
        id: str | None = None,
        starts_at: int = 0,
        expires_at: int = 0,
        memo: str | None = None,
    ) -> bool:
        ad_id = self._ad_id or id
        if ad_id is None:
            raise ParameterError('ad_idは必須です')
        data = {
            'id': ad_id,
            'url': url,
            'memo': memo or '',
            'place': place,
            'priority': priority,
            'ratio': ratio,
            'startsAt': starts_at,
            'expiresAt': expires_at,
            'imageUrl': image_url,
        }
        res: bool = await self._session.request(
            Route('POST', '/api/admin/ad/update'), json=data, auth=True, lower=True
        )
        return res

    async def delete(self, id: str | None = None) -> bool:
        ad_id = self._ad_id or id
        res: bool = await self._session.request(
            Route('POST', '/api/admin/ad/delete'), json={'id': ad_id}, auth=True, lower=True
        )
        return res


class AdminAdvertisingActions(AdminAdvertisingModelActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        url: str,
        place: Literal['square', 'horizontal', 'horizontal-big'],
        priority: Literal['high', 'middle', 'low'],
        ratio: int,
        image_url: str,
        starts_at: int = 0,
        expires_at: int = 0,
        memo: str | None = None,
    ) -> bool:
        data = {
            'url': url,
            'memo': memo or '',
            'place': place,
            'priority': priority,
            'ratio': ratio,
            'startsAt': starts_at,
            'expiresAt': expires_at,
            'imageUrl': image_url,
        }
        res: bool = await self._session.request(
            Route('POST', '/api/admin/ad/create'), json=data, auth=True, lower=True
        )
        return res

    async def get_list(
        self, limit: int = 10, since_id: str | None = None, until_id: str | None = None
    ) -> AsyncGenerator[Ad, None]:
        if self._client._config.use_version < 13:
            raise NotSupportVersion(NotSupportVersionText)

        async def request(body) -> list[Ad]:
            res: list[IAd] = await self._session.request(
                Route('POST', '/api/admin/ad/list'), lower=True, auth=True, json=body,
            )
            return [Ad(ad, client=self._client) for ad in res]

        data = {'limit': limit, 'sinceId': since_id, 'untilId': until_id}
        if all:
            data['limit'] = 100
        first_req = await request(data)
        for ad in first_req:
            yield ad

        if all and len(first_req) == 100:
            data['untilId'] = first_req[-1].id
            while True:
                res = await request(data)
                if len(res) <= 100:
                    for ad in res:
                        yield ad
                if len(res) == 0:
                    break
                data['untilId'] = res[-1].id
