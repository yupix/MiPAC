from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.actions.admins.accounts import AdminAccountActions

from mipac.actions.admins.user import ClientAdminUserActions, AdminUserActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientAdminUserManager:
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        self.account: AdminAccountActions = AdminAccountActions(session=session, client=client)
        self.__action: ClientAdminUserActions = ClientAdminUserActions(
            user_id=user_id, session=session, client=client
        )

    @property
    def action(self) -> ClientAdminUserActions:
        return self.__action


class AdminUserManager:
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminUserActions:
        return AdminUserActions(session=self.__session, client=self.__client)
