from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.meta import AdminMeta
from mipac.types.meta import IAdminMeta

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_meta(self, detail: bool = False) -> AdminMeta:
        res: IAdminMeta = await self.__session.request(
            Route('POST', '/api/admin/meta'),
            json={'detail': detail},
            auth=True,
            lower=True,
        )
        return AdminMeta(res, client=self.__client)

    async def get_invite(self) -> bool:
        return bool(
            await self.__session.request(Route('POST', '/api/admin/invite'))
        )
