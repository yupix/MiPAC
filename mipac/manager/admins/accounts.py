from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.admins.accounts import AdminAccountActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminAccountManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__action: AdminAccountActions = AdminAccountActions(session=session, client=client)

    @property
    def action(self) -> AdminAccountActions:
        return self.__action
