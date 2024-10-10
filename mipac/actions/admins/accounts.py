from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.user import CreatedUser
from mipac.types.user import ICreatedUser

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminAccountActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(self, username: str, password: str, setup_password: str | None=None) -> CreatedUser:
        """ユーザーを作成します

        Endpoint: `/api/admin/accounts/create`

        Parameters
        ----------
        username : str
            ユーザー名
        password : str
            パスワード
        setup_password : str, optional
            セットアップパスワード, by default None

        Returns
        -------
        CreatedUser
            作成されたユーザー
        """
        data = {"username": username, "password": password, "setupPassword": setup_password}
        raw_created_user: ICreatedUser = await self._session.request(
            Route("POST", "/api/admin/accounts/create"),
            json=data,
        )
        return CreatedUser(raw_created_user, client=self._client)

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
