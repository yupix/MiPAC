from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.mute import MuteUser
from mipac.types.mute import IMuteUser
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MuteActions(AbstractAction):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self._user_id: str | None = user_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

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
        data = {"userId": user_id}
        res: bool = await self._session.request(
            Route("POST", "/api/mute/create"), auth=True, json=data
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
        data = {"userId": user_id}
        res: bool = await self._session.request(
            Route("POST", "/api/mute/delete"), auth=True, json=data
        )
        return res

    async def gets(
        self,
        limit: int = 100,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = True,
    ) -> AsyncGenerator[MuteUser, None]:
        if limit > 100:
            raise ParameterError("limit は100以下である必要があります")

        if get_all:
            limit = 100

        body = remove_dict_empty({"limit": limit, "sinceId": since_id, "untilId": until_id})

        pagination = Pagination[IMuteUser](
            self._session, Route("POST", "/api/mute/list"), json=body
        )

        while True:
            raw_mute_users = await pagination.next()
            for raw_mute_user in raw_mute_users:
                yield MuteUser(raw_mute_user, client=self._client)

            if get_all is False or pagination.is_final:
                break
