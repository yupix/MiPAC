
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.app import AppActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AppManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: AppActions = AppActions(session=session, client=client)

    @property
    def action(self) -> AppActions:
        return self.__action
