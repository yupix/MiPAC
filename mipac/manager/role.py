from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.role import RoleActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class RoleManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> RoleActions:
        return RoleActions(session=self.__session, client=self.__client)
