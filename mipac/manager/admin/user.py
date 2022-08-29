from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientActions
    from mipac.models.user import UserDetailed


class AdminUserManager:
    def __init__(
        self,
        user_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__user_id = user_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def delete_account(self, user_id: Optional[str] = None) -> bool:
        """
        Deletes the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be deleted
        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/accounts/delete'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def show_user(self, user_id: Optional[str] = None) -> UserDetailed:
        """
        Shows the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be shown

        Returns
        -------
        UserDetailed
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('GET', '/api/admin/show-user'),
            json=data,
            auth=True,
            lower=True,
        )
        return UserDetailed(res, client=self.__client)

    async def suspend(self, user_id: Optional[str] = None) -> bool:
        """
        Suspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be suspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/suspend-user'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def unsuspend(self, user_id: Optional[str] = None) -> bool:
        """
        Unsuspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be unsuspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res: bool = await self.__session.request(
            Route('POST', '/api/admin/unsuspend-user'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)
