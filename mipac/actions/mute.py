from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class MuteActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self._user_id: str | None = user_id
        self._session: HTTPClient = session
        self._client: ClientActions = client

    async def add(self, user_id: str | None = None) -> bool:
        """
        Adds the specified user as a mute target

        Parameters
        ----------
        user_id : str | None, optional
            Mute target user Id, by default None

        Returns
        -------
        bool
            Whether the mute was successful or not
        """

        user_id = user_id or self._user_id
        data = {'userId': user_id}
        res: bool = await self._session.request(
            Route('POST', '/api/mute/create'), auth=True, json=data
        )
        return res

    async def delete(self, user_id: str | None = None) -> bool:
        """
        Unmute the specified user

        Parameters
        ----------
        user_id : str | None, optional
            Unmute target user Id, by default None

        Returns
        -------
        bool
            Whether the unmute was successful or not.
        """

        user_id = user_id or self._user_id
        data = {'userId': user_id}
        res: bool = await self._session.request(
            Route('POST', '/api/mute/delete'), auth=True, json=data
        )
        return res
