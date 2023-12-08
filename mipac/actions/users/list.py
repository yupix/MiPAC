from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.user import UserList
from mipac.types.user import IUserList

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientListActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client


class UserListActions(ClientListActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(self, name: str) -> UserList:
        """Create a new user list
        
        Endpoint `/api/users/lists/create`

        Parameters
        ----------
        name : str
            The name of the new user list
        
        Returns
        -------
        UserList
            The created user list
        """
        raw_user_list: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/create"),
            json={"name": name},
            auth=True
        )
        return UserList(raw_user_list=raw_user_list, client=self._client)
