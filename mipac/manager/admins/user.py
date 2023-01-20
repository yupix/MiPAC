from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.actions.admins.user import AdminUserActions

from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminUserManager:
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminUserActions:
        return AdminUserActions(
            user_id=self.__user_id, session=self.__session, client=self.__client
        )
