from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.ad import AdminAdvertisingActions, AdminAdvertisingModelActions
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ("AdminAdvertisingManager", "AdminAdvertisingModelManager")


class AdminAdvertisingModelManager(AbstractManager):
    def __init__(self, ad_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__ad_id: str | None = ad_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminAdvertisingModelActions:
        return AdminAdvertisingModelActions(
            ad_id=self.__ad_id, session=self.__session, client=self.__client
        )


class AdminAdvertisingManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminAdvertisingActions:
        return AdminAdvertisingActions(session=self.__session, client=self.__client)

    async def create(
        self,
        url: str,
        memo: str,
        place: str,
        priority: Literal["high", "middle", "low"],
        ratio: str,
        expires_at: int,
        image_url: str,
    ):
        data = {
            "url": url,
            "memo": memo,
            "place": place,
            "priority": priority,
            "ratio": ratio,
            "expires_at": expires_at,
            "image_url": image_url,
        }
        return await self.__session.request(
            Route("POST", "/api/admin/ad/create"),
            json=data,
            auth=True,
            lower=True,
        )
