from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.user import MeDetailed, UserDetailedNotMe, packed_user

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminUserActions(AbstractAction):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id = user_id
        self.__session = session
        self.__client = client

    async def delete_account(self, user_id: str | None = None) -> bool:
        """
        Deletes the user with the specified user ID.

        Parameters
        ----------
        user_id : str | None, default=None
            ID of the user to be deleted
        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id

        data = {"userId": user_id}
        res = await self.__session.request(
            Route("POST", "/api/admin/accounts/delete"),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def show_user(self, user_id: str | None = None) -> UserDetailedNotMe | MeDetailed:
        """
        Shows the user with the specified user ID.

        Parameters
        ----------
        user_id : str | None, default=None
            ID of the user to be shown

        Returns
        -------
        UserDetailedNotMe | MeDetailed
        """

        user_id = user_id or self.__user_id
        data = {"userId": user_id}
        res = await self.__session.request(
            Route("GET", "/api/admin/show-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return packed_user(res, client=self.__client)

    async def suspend(self, user_id: str | None = None) -> bool:
        """
        Suspends the user with the specified user ID.

        Parameters
        ----------
        user_id : str | None, default=None
            ID of the user to be suspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {"userId": user_id}
        res = await self.__session.request(
            Route("POST", "/api/admin/suspend-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def unsuspend(self, user_id: str | None = None) -> bool:
        """
        Unsuspends the user with the specified user ID.

        Parameters
        ----------
        user_id : str | None, default=None
            ID of the user to be unsuspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {"userId": user_id}
        res: bool = await self.__session.request(
            Route("POST", "/api/admin/unsuspend-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)
