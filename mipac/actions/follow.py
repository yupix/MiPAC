from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.follow import FollowRequest
from mipac.models.user import PartialUser
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.types.user import IPartialUser


class SharedFollowActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session = session
        self._client = client

    async def add(self, *, user_id: str) -> PartialUser:
        """
        Follow a user

        Returns
        -------
        UserLite:
            The user that you followed
        """
        data = {"userId": user_id}
        res: IPartialUser = await self._session.request(
            Route("POST", "/api/following/create"),
            json=data,
            auth=True,
            lower=True,
        )
        return PartialUser(res, client=self._client)

    async def remove(self, *, user_id: str) -> PartialUser:
        """
        Unfollow a user

        Returns
        -------
        PartialUser
            The user that you unfollowed
        """
        data = {"userId": user_id}
        raw_user: IPartialUser = await self._session.request(
            Route("POST", "/api/following/delete"), json=data, auth=True
        )
        return PartialUser(raw_user=raw_user, client=self._client)

    async def invalidate(self, *, user_id: str) -> PartialUser:
        """
        Make the user unfollows you

        Returns
        -------
        PartialUser
            The user that followed you
        """
        data = {"userId": user_id}
        res: IPartialUser = await self._session.request(
            Route("POST", "/api/following/invalidate"), json=data, auth=True
        )
        return PartialUser(res, client=self._client)


class ClientFollowActions(SharedFollowActions):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user_id: str = user_id

    @override
    async def add(self, *, user_id: str | None = None) -> PartialUser:
        """
        Follow a user

        Returns
        -------
        UserLite:
            The user that you followed
        """

        user_id = user_id or self.__user_id

        return await super().add(user_id=user_id)

    @override
    async def remove(self, *, user_id: str | None = None) -> PartialUser:
        """
        Unfollow a user

        Returns
        -------
        PartialUser
            The user that you unfollowed
        """

        user_id = user_id or self.__user_id

        return await super().remove(user_id=user_id)

    @override
    async def invalidate(self, *, user_id: str | None = None) -> PartialUser:
        """
        Make the user unfollows you

        Returns
        -------
        PartialUser
            The user that followed you
        """

        user_id = user_id or self.__user_id

        return await super().invalidate(user_id=user_id)


class FollowActions(SharedFollowActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)


class FollowRequestActions(AbstractAction):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self._session = session
        self._client = client

    async def get_all(self) -> list[FollowRequest]:
        """
        Get all follow requests

        Returns
        -------
        list[FollowRequest]
            List of follow requests
        """

        res: list[IFollowRequest] = await self._session.request(
            Route("POST", "/api/following/requests/list"),
            auth=True,
            lower=True,
        )
        return [FollowRequest(follow_request=i, client=self._client) for i in res]

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

        data = {"userId": user_id}
        return bool(
            await self._session.request(
                Route("POST", "/api/following/requests/accept"),
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

        data = {"userId": user_id}
        return bool(
            await self._session.request(
                Route("POST", "/api/following/requests/reject"),
                json=data,
                auth=True,
            )
        )

    async def cancel(self, user_id: str | None = None) -> PartialUser:
        """
        Cancel a follow request

        Parameters
        ----------
        user_id: str
            The user ID to cancel

        Returns
        -------
        PartialUser
            The user that you canceled to follow
        """

        user_id = user_id or self.__user_id

        data = {"userId": user_id}
        res: IPartialUser = await self._session.request(
            Route("POST", "/api/following/requests/cancel"),
            json=data,
            auth=True,
            lower=True,
        )
        return PartialUser(res, client=self._client)
