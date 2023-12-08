from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.user import UserList
from mipac.types.user import IUserList

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientPartialUserListActions(AbstractAction):
    """ユーザー向けのリストのアクションを提供します。"""
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_list(self, *, user_id: str | None = None) -> list[UserList]:
        """Get the user lists of a user

        Endpoint `/api/users/lists/list`

        Parameters
        ----------
        user_id : str
            The id of the user to get the lists of

        Returns
        -------
        list[UserList]
            The user lists the user has
        """

        user_id = user_id or self.__user_id

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        raw_user_lists: list[IUserList] = await self._session.request(
            Route("POST", "/api/users/lists/list"), json={"userId": user_id}, auth=True
        )

        return [UserList(raw_user_list, client=self._client) for raw_user_list in raw_user_lists]

    async def pull(self, list_id: str, *, user_id: str | None = None) -> bool:
        """Pull a user from a user list

        Endpoint `/api/users/lists/pull`

        Parameters
        ----------
        list_id : str
            The id of the user list to pull from
        user_id : str, optional
            The id of the user to pull, by default None

        Returns
        -------
        bool
            True if the user was pulled, False otherwise
        """
        user_id = user_id or self.__user_id

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/pull"),
            json={"listId": list_id, "userId": user_id},
            auth=True,
        )
        return res


class ClientUserListActions(ClientPartialUserListActions):
    def __init__(
        self,
        list_id: str | None = None,
        *,
        user_id: str | None = None,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(user_id=user_id, session=session, client=client)
        self.__list_id: str | None = list_id

    async def delete(self, *, list_id: str | None = None) -> bool:
        """Delete a user list

        Endpoint `/api/users/lists/delete`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to delete, by default None

        Returns
        -------
        bool
            True if the user list was deleted, False otherwise
        """
        list_id = list_id or self.__list_id

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/delete"), json={"listId": list_id}, auth=True
        )
        return res

    @override
    async def get_list(self, user_id: str) -> list[UserList]:
        return await super().get_list(user_id=user_id)

    @override
    async def pull(self, user_id: str, *, list_id: str | None = None) -> bool:
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        return await super().pull(list_id=list_id, user_id=user_id)


class UserListActions(ClientUserListActions):
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
            Route("POST", "/api/users/lists/create"), json={"name": name}, auth=True
        )
        return UserList(raw_user_list=raw_user_list, client=self._client)

    @override
    async def delete(self, list_id: str) -> bool:
        return await super().delete(list_id=list_id)

    @override
    async def pull(self, list_id: str, user_id: str) -> bool:
        return await super().pull(list_id=list_id, user_id=user_id)
