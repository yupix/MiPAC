from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abc.manager import AbstractManager
from mipac.actions.my import MyActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class MyManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientActions):
        self.__session = session
        self.__client = client

    @property
    def action(self):
        return MyActions(session=self.__session, client=self.__client)
