
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.users.list import ClientListActions, UserListActions


if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

class ClientUserListManager(AbstractManager):
    def __init__(self, list_id: str, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientListActions = ClientListActions(list_id=list_id, session=self.__session, client=self.__client)

    @property
    def action(self) -> ClientListActions:
        return self.__action



class UserListManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: UserListActions = UserListActions(session=self.__session, client=self.__client)

    @property
    def action(self) -> UserListActions:
        return self.__action
