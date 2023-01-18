from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterable

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.mute import MuteUser
from mipac.types.mute import IMuteUser
from mipac.util import remove_dict_empty

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MuteActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
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

    async def gets(
        self,
        limit: int = 100,
        since_id: str | None = None,
        until_id: str | None = None,
        all: bool = True,
    ) -> AsyncIterable[MuteUser]:
        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        async def request(body) -> list[MuteUser]:
            res: list[IMuteUser] = await self._session.request(
                Route('POST', '/api/mute/list'),
                lower=True,
                auth=True,
                json=body,
            )
            return [MuteUser(user, client=self._client) for user in res]

        data = remove_dict_empty(
            {'limit': limit, 'sinceId': since_id, 'untilId': until_id}
        )

        if all:
            data['limit'] = 100
        first_req = await request(data)

        for user in first_req:
            yield user

        if all and len(first_req) == 100:
            data['untilId'] = first_req[-1].id
            while True:
                res = await request(data)
                if len(res) <= 100:
                    for user in res:
                        yield user
                if len(res) == 0:
                    break
                data['untilId'] = res[-1].id
