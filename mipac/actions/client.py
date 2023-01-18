from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.lite.meta import LiteMeta
from mipac.models.meta import Meta
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
