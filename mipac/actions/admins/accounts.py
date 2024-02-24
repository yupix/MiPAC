from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminAccountActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(self, username: str, password: str):  # TODO: 多分UserDetailed + tokenってキー
        """ユーザーを作成します

        Endpoint: `/api/admin/accounts/create`

        Parameters
        ----------
        username : str
            ユーザー名
        password : str
            パスワード
        """

        data = {"username": username, "password": password}
        res = await self._session.request(
            Route("POST", "/api/admin/accounts/create"),
            json=data,
        )
        return res

    async def delete(self, *, user_id: str) -> bool:
        """対象のユーザーを削除します

        Endpoint: `/api/admin/accounts/delete`

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """
        res = await self._session.request(
            Route("POST", "/api/admin/accounts/delete"),
            json={"userId": user_id},
            auth=True,
            lower=True,
        )
        return bool(res)
