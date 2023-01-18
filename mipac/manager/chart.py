from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.chart import ChartActions

if TYPE_CHECKING:
    from mipac.client import ClientManager
    from mipac.http import HTTPClient

__all__ = ('ChartManager',)


class ChartManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ChartActions:
        return ChartActions(session=self.__session, client=self.__client)
