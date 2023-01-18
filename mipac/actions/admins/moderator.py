from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import Route

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class AdminModeratorActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__user_id: str | None = user_id

    async def add(self, user_id: str | None = None) -> bool:
        """
        Add a user as a moderator

        Parameters
        ----------
        user_id : str | None, default=None
            ユーザーのID

        Returns
        -------
        bool
            成功したか否か
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/moderators/add'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def remove(self, user_id: str | None = None) -> bool:
        """
        Unmoderate a user

        Parameters
        ----------
        user_id : str | None, default=None
            ユーザーのID

        Returns
        -------
        bool
            成功したか否か
        """
        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/moderators/remove'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)
