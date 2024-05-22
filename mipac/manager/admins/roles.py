from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.roles import AdminRoleActions, ClientAdminRoleActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientAdminRoleManager(AbstractManager):
    def __init__(self, role_id: str, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientAdminRoleActions = ClientAdminRoleActions(
            role_id=role_id, session=self.__session, client=self.__client
        )

    @property
    def action(self) -> ClientAdminRoleActions:
        return self.__action


class AdminRoleManager:
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__action: AdminRoleActions = AdminRoleActions(session=session, client=client)

    @property
    def action(self) -> AdminRoleActions:
        return self.__action
