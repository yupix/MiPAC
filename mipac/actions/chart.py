from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.chart import ActiveUsersChart, DriveChart

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ChartActions(AbstractAction):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_active_user(
        self, span: str = 'day', limit: int = 30, offset: int = 0
    ) -> ActiveUsersChart:
        data = {'span': span, 'limit': limit, 'offset': offset}
        data = await self.__session.request(
            Route('POST', '/api/charts/active-users'),
            json=data,
            auth=True,
            lower=True,
        )
        return ActiveUsersChart(data)

    async def get_drive(
        self, span: str = 'day', limit: int = 30, offset: int = 0
    ) -> DriveChart:
        data = {'span': span, 'limit': limit, 'offset': offset}
        data = await self.__session.request(
            Route('POST', '/api/charts/drive'),
            json=data,
            auth=True,
            lower=True,
        )
        return DriveChart(data)
