from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedAdminUserActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session = session
        self._client = client

    @deprecated
    async def delete_account(self, *, user_id: str) -> bool:
        """対象のユーザーを削除します

        Endpoint: `/api/admin/accounts/delete`

        .. deprecated:: 0.6.2
            Use :meth:`mipac.actions.admins.accounts.delete` instead.

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """
        return await self._client.admin.account.action.delete(user_id=user_id)

    async def show_user(self, *, user_id: str):  # TODO: 専用の型が必要
        """ユーザーの情報を取得します

        Parameters
        ----------
        user_id : str
            対象のユーザーID
        """
        data = {"userId": user_id}

        raw_user = await self._session.request(
            Route("GET", "/api/admin/show-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return raw_user

    async def suspend(self, *, user_id: str) -> bool:
        """対象のユーザーを凍結します

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """
        data = {"userId": user_id}

        res: bool = await self._session.request(
            Route("POST", "/api/admin/suspend-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return res

    async def unsuspend(self, *, user_id: str) -> bool:
        """ユーザーの凍結を解除します

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """
        data = {"userId": user_id}

        res: bool = await self._session.request(
            Route("POST", "/api/admin/unsuspend-user"),
            json=data,
            auth=True,
            lower=True,
        )
        return res


class ClientAdminUserActions(SharedAdminUserActions):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user_id = user_id

    @override
    async def delete_account(self, *, user_id: str | None = None) -> bool:
        user_id = user_id or self.__user_id

        return await super().delete_account(user_id=user_id)

    @override
    async def show_user(self, *, user_id: str | None = None):
        """ユーザーの情報を取得します

        Parameters
        ----------
        user_id : str
            対象のユーザーID
        """
        user_id = user_id or self.__user_id

        return await super().show_user(user_id=user_id)

    @override
    async def suspend(self, *, user_id: str | None = None) -> bool:
        """対象のユーザーを凍結します

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """

        user_id = user_id or self.__user_id

        return await super().suspend(user_id=user_id)

    @override
    async def unsuspend(self, *, user_id: str | None = None) -> bool:
        """ユーザーの凍結を解除します

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            成功ならTrue
        """
        user_id = user_id or self.__user_id

        return await super().unsuspend(user_id=user_id)


class AdminUserActions(SharedAdminUserActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
