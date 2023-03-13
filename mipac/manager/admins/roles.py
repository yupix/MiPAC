from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.roles import AdminRoleActions, AdminRoleModelActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminRolesModelManager(AbstractManager):
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__role_id = role_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminRoleModelActions:
        return AdminRoleModelActions(
            role_id=self.__role_id, session=self.__session, client=self.__client
        )


class AdminRolesManager:
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__role_id = role_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminRoleActions:
        return AdminRoleActions(
            role_id=self.__role_id, session=self.__session, client=self.__client
        )
