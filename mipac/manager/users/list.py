from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.users.list import (
    ClientPartialUserListActions,
    ClientUserListActions,
    UserListActions,
)
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientPartialUserListManager(AbstractManager):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientPartialUserListActions = ClientPartialUserListActions(
            user_id=self.__user_id, session=self.__session, client=self.__client
        )

    @property
    def action(self) -> ClientPartialUserListActions:
        return self.__action


class ClientUserListManager(AbstractManager):
    def __init__(
        self,
        list_id: str,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientUserListActions = ClientUserListActions(
            list_id=list_id, session=self.__session, client=self.__client
        )

    @property
    def action(self) -> ClientUserListActions:
        return self.__action


class UserListManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: UserListActions = UserListActions(
            session=self.__session, client=self.__client
        )

    @property
    def action(self) -> UserListActions:
        return self.__action
