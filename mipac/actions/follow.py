from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import Route
from mipac.models.follow import FollowRequest
from mipac.models.user import UserDetailed
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientActions


class FollowActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__user_id: str | None = user_id
        self.__session = session
        self.__client = client

    async def add(self, user_id: str | None = None) -> tuple[bool, str | None]:
        """
        ユーザーをフォローします

        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/following/create'),
            json=data,
            auth=True,
            lower=True,
        )
        if res.get('error'):
            code = res['error']['code']
            status = False
        else:
            code = None
            status = True
        return status, code

    async def remove(self, user_id: str | None = None) -> bool:
        """
        ユーザーのフォローを解除します

        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res: bool = await self.__session.request(
            Route('POST', '/api/following/delete'), json=data, auth=True
        )
        return res


class FollowRequestActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__user_id: str | None = user_id
        self.__session = session
        self.__client = client

    async def get_all(self) -> list[FollowRequest]:
        """
        未承認のフォローリクエストを取得します
        """

        res: list[IFollowRequest] = await self.__session.request(
            Route('POST', '/api/following/requests/list'),
            auth=True,
            lower=True,
        )
        return [
            FollowRequest(follow_request=i, client=self.__client) for i in res
        ]

    async def get_user(self, user_id: str | None = None) -> UserDetailed:
        """
        フォローリクエスト元のユーザーを取得します
        Parameters
        ----------
        user_id : str | None, default=None
            ユーザーID

        Returns
        -------
        UserDetailed
            フォローリクエスト元のユーザー
        """

        user_id = user_id or self.__user_id

        return await self.__client.user.action.get(user_id)

    async def accept(self, user_id: str | None = None) -> bool:
        """
        与えられたIDのユーザーのフォローリクエストを承認します
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/following/requests/accept'),
                json=data,
                auth=True,
            )
        )

    async def reject(self, user_id: str | None) -> bool:
        """
        与えられたIDのユーザーのフォローリクエストを拒否します
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/following/requests/reject'),
                json=data,
                auth=True,
            )
        )
