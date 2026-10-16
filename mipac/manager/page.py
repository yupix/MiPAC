from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientManager


class PagesManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_pages(
        self,
        limit: int = 100,
        since_id: str | None = None,
        until_id: str | None = None,
    ):
        data = {"limit": limit, "sinceId": since_id, "untilId": until_id}
        res = await self.__session.request(Route("POST", "/api/i/pages"), json=data, auth=True)
        return res
