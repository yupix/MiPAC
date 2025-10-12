from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.ad import AdminAdActions, ClientAdminAdActions
from mipac.http import HTTPClient, Route
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ("AdminAdManager", "ClientAdminAdManager")


class ClientAdminAdManager(AbstractManager):
    def __init__(self, ad_id: str, *, session: HTTPClient, client: ClientManager):
        self.__ad_id: str = ad_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ClientAdminAdActions:
        return ClientAdminAdActions(
            ad_id=self.__ad_id, session=self.__session, client=self.__client
        )


class AdminAdManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminAdActions:
        return AdminAdActions(session=self.__session, client=self.__client)

    @deprecated
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
        """
        ... deprecated
        Use `AdminAdActions.create` instead
        責務違反の為 0.8.0 で削除予定
        """
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
