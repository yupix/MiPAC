from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import Route
from mipac.models.follow import FollowRequest
from mipac.models.user import LiteUser
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager
    from mipac.types.user import ILiteUser


class FollowActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__user_id: str | None = user_id
        self.__session = session
        self.__client = client

    async def add(self, user_id: str | None = None) -> LiteUser:
        """
        Follow a user

        Returns
        -------
        UserLite:
            The user that you followed
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res: ILiteUser = await self.__session.request(
            Route('POST', '/api/following/create'),
            json=data,
            auth=True,
            lower=True,
        )
        return LiteUser(res, client=self.__client)

    async def remove(self, user_id: str | None = None) -> LiteUser:
        """
        Unfollow a user

        Returns
        -------
        LiteUser
            The user that you unfollowed
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/following/delete'), json=data, auth=True
        )
        return LiteUser(res, client=self.__client)

    async def invalidate(self, user_id: str | None = None) -> LiteUser:
        """
        Make the user unfollows you

        Returns
        -------
        LiteUser
            The user that followed you
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res: ILiteUser = await self.__session.request(
            Route('POST', '/api/following/invalidate'), json=data, auth=True
        )
        return LiteUser(res, client=self.__client)


class FollowRequestActions(AbstractAction):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__user_id: str | None = user_id
        self.__session = session
        self.__client = client

    async def get_all(self) -> list[FollowRequest]:
        """
        Get all follow requests

        Returns
        -------
        list[FollowRequest]
            List of follow requests
        """

        res: list[IFollowRequest] = await self.__session.request(
            Route('POST', '/api/following/requests/list'),
            auth=True,
            lower=True,
        )
        return [
            FollowRequest(follow_request=i, client=self.__client) for i in res
        ]

    async def accept(self, user_id: str | None = None) -> bool:
        """
        Accept a follow request

        Parameters
        ----------
        user_id: str
            The user ID to accept

        Returns
        -------
        bool
            Whether the request was accepted
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

    async def reject(self, user_id: str | None = None) -> bool:
        """
        Reject a follow request

        Parameters
        ----------
        user_id: str
            The user ID to reject

        Returns
        -------
        bool
            Whether the request was rejected
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

    async def cancel(self, user_id: str | None = None) -> LiteUser:
        """
        Cancel a follow request

        Parameters
        ----------
        user_id: str
            The user ID to cancel

        Returns
        -------
        LiteUser
            The user that you canceled to follow
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res: ILiteUser = await self.__session.request(
            Route('POST', '/api/following/requests/cancel'),
            json=data,
            auth=True,
            lower=True,
        )
        return LiteUser(res, client=self.__client)
