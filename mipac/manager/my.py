from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.my import MyActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MyManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    @property
    def action(self):
        return MyActions(session=self.__session, client=self.__client)
