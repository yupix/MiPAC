from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abc.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.follow import FollowRequest
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class MyActions(AbstractAction):
    def __init__(self, session: HTTPClient, client: ClientActions):
        self.__session = session
        self.__client = client

    async def fetch_follow_requests(self):
        res: list[IFollowRequest] = await self.__session.request(
            Route('POST', '/api/following/requests/list'),
            auth=True,
            lower=True,
        )
        return [FollowRequest(i, client=self.__client) for i in res]
