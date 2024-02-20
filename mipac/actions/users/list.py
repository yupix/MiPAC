from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.models.user import UserList, UserListMembership
from mipac.types.user import IUserList, IUserListMembership
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedPartialUserListActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_list(self, *, user_id: str) -> list[UserList]:
        """Get the user lists of a user

        Endpoint `/api/users/lists/list`

        Parameters
        ----------
        user_id : str
            The id of the user to get the lists of

        Returns
        -------
        list[UserList]
            The user lists the user has
        """
        raw_user_lists: list[IUserList] = await self._session.request(
            Route("POST", "/api/users/lists/list"), json={"userId": user_id}, auth=True
        )

        return [UserList(raw_user_list, client=self._client) for raw_user_list in raw_user_lists]

    async def pull(self, *, list_id: str, user_id: str) -> bool:
        """Pull a user from a user list

        Endpoint `/api/users/lists/pull`

        Parameters
        ----------
        list_id : str
            The id of the user list to pull from
        user_id : str, optional
            The id of the user to pull, by default None

        Returns
        -------
        bool
            True if the user was pulled, False otherwise
        """
        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/pull"),
            json={"listId": list_id, "userId": user_id},
            auth=True,
        )
        return res

    async def push(self, *, list_id: str, user_id: str) -> bool:
        """Push a user to a user list

        Endpoint `/api/users/lists/push`

        Parameters
        ----------
        list_id : str
            The id of the user list to push to
        user_id : str, optional
            The id of the user to push, by default None

        Returns
        -------
        bool
            True if the user was pushed, False otherwise
        """
        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/push"),
            json={"listId": list_id, "userId": user_id},
            auth=True,
        )
        return res

    async def update_membership(self, with_replies: bool = MISSING, *, list_id: str, user_id: str):
        data = remove_dict_missing(
            {"listId": list_id, "userId": user_id, "withReplies": with_replies}
        )

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/update-membership"),
            json=data,
            auth=True,
        )
        return res


class ClientPartialUserListActions(SharedPartialUserListActions):
    """ユーザー向けのリストのアクションを提供します。"""

    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user_id: str = user_id

    @override
    async def get_list(self, *, user_id: str | None = None) -> list[UserList]:
        """Get the user lists of a user

        Endpoint `/api/users/lists/list`

        Parameters
        ----------
        user_id : str
            The id of the user to get the lists of

        Returns
        -------
        list[UserList]
            The user lists the user has
        """
        user_id = user_id or self.__user_id
        return await super().get_list(user_id=user_id)

    @override
    async def pull(self, *, list_id: str, user_id: str | None = None) -> bool:
        """Pull a user from a user list

        Endpoint `/api/users/lists/pull`

        Parameters
        ----------
        list_id : str
            The id of the user list to pull from
        user_id : str, optional
            The id of the user to pull, by default None

        Returns
        -------
        bool
            True if the user was pulled, False otherwise
        """
        user_id = user_id or self.__user_id

        return await super().pull(list_id=list_id, user_id=user_id)

    @override
    async def push(self, *, list_id: str, user_id: str | None = None) -> bool:
        """Push a user to a user list

        Endpoint `/api/users/lists/push`

        Parameters
        ----------
        list_id : str
            The id of the user list to push to
        user_id : str, optional
            The id of the user to push, by default None

        Returns
        -------
        bool
            True if the user was pushed, False otherwise
        """
        user_id = user_id or self.__user_id

        return await super().push(list_id=list_id, user_id=user_id)

    @override
    async def update_membership(
        self, with_replies: bool = MISSING, *, list_id: str, user_id: str | None = None
    ):
        user_id = user_id or self.__user_id

        return await super().update_membership(
            list_id=list_id, with_replies=with_replies, user_id=user_id
        )


class SharedUserListActions(SharedPartialUserListActions):
    def __init__(
        self,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)

    async def delete(self, *, list_id: str) -> bool:
        """Delete a user list

        Endpoint `/api/users/lists/delete`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to delete, by default None

        Returns
        -------
        bool
            True if the user list was deleted, False otherwise
        """
        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/delete"), json={"listId": list_id}, auth=True
        )
        return res

    async def show(self, for_public: bool = False, *, list_id: str) -> UserList:
        """Show a user list

        Endpoint `/api/users/lists/show`

        Parameters
        ----------
        for_public : bool, optional
            Whether to show the user list for the public, by default False
        list_id : str, optional
            The id of the user list to show, by default None

        Returns
        -------
        UserList
            The user list
        """
        raw_user_list: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/show"),
            json={"listId": list_id, "forPublic": for_public},
            auth=True,
        )
        return UserList(raw_user_list=raw_user_list, client=self._client)

    async def favorite(self, *, list_id: str) -> bool:
        """Favorite a user list

        Endpoint `/api/users/lists/favorite`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to favorite, by default None

        Returns
        -------
        bool
            True if the user list was favorited, False otherwise
        """
        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/favorite"), json={"listId": list_id}, auth=True
        )
        return res

    async def unfavorite(self, *, list_id: str | None = None) -> bool:
        """Unfavorite a user list

        Endpoint `/api/users/lists/unfavorite`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to unfavorite, by default None

        Returns
        -------
        bool
            True if the user list was unfavorited, False otherwise
        """
        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/unfavorite"), json={"listId": list_id}, auth=True
        )
        return res

    async def update(
        self, name: str = MISSING, is_public: bool = MISSING, *, list_id: str
    ) -> UserList:
        """Update a user list

        Endpoint `/api/users/lists/update`

        Parameters
        ----------
        name : str, optional
            The new name of the user list, by default MISSING
        is_public : bool, optional
            Whether the user list should be public, by default MISSING
        list_id : str, optional
            The id of the user list to update, by default None

        Returns
        -------
        UserList
            The updated user list
        """
        data = remove_dict_missing({"listId": list_id, "name": name, "public": is_public})

        res: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/update"),
            json=data,
            auth=True,
        )
        return UserList(raw_user_list=res, client=self._client)

    async def create_from_public(self, name: str, *, list_id: str):
        res: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/create-from-public"),
            json={"listId": list_id, "name": name},
            auth=True,
        )
        return UserList(raw_user_list=res, client=self._client)

    async def get_memberships(
        self,
        for_public: bool = False,
        limit: int = 30,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        list_id: str,
    ) -> list[UserListMembership]:
        data = {
            "listId": list_id,
            "forPublic": for_public,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        raw_user_list_memberships: list[IUserListMembership] = await self._session.request(
            Route("POST", "/api/users/lists/get-memberships"),
            json=data,
            auth=True,
        )

        return [
            UserListMembership(raw_user_list_membership, client=self._client)
            for raw_user_list_membership in raw_user_list_memberships
        ]

    async def get_all_memberships(
        self,
        for_public: bool = False,
        limit: int = 30,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        list_id: str,
    ):
        data = {
            "listId": list_id,
            "forPublic": for_public,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }
        pagination = Pagination[IUserListMembership](
            http_client=self._session,
            route=Route("POST", "/api/users/lists/get-memberships"),
            json=data,
            auth=True,
        )

        while pagination.is_final is False:
            raw_user_list_memberships = await pagination.next()
            for raw_user_list_membership in raw_user_list_memberships:
                yield UserListMembership(raw_user_list_membership, client=self._client)

    # ここからはusers/lists系じゃないが、ここにあってほしい物
    async def get_time_line(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
        *,
        list_id: str,
    ) -> list[Note]:
        return await self._client.note.action.get_time_line(
            list_id=list_id,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            include_renote_my_notes=include_renote_my_notes,
            include_local_renotes=include_local_renotes,
            with_renotes=with_renotes,
            with_files=with_files,
        )

    async def get_all_time_line(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
        *,
        list_id: str,
    ):
        async for i in self._client.note.action.get_all_time_line(
            list_id=list_id,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            include_renote_my_notes=include_renote_my_notes,
            include_local_renotes=include_local_renotes,
            with_renotes=with_renotes,
            with_files=with_files,
        ):
            yield i


class ClientUserListActions(SharedUserListActions):
    def __init__(
        self,
        list_id: str,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)
        self.__list_id: str = list_id

    @override
    async def delete(self, *, list_id: str | None = None) -> bool:
        """Delete a user list

        Endpoint `/api/users/lists/delete`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to delete, by default None

        Returns
        -------
        bool
            True if the user list was deleted, False otherwise
        """
        list_id = list_id or self.__list_id

        return await super().delete(list_id=list_id)

    @override
    async def show(self, for_public: bool = False, *, list_id: str | None = None) -> UserList:
        """Show a user list

        Endpoint `/api/users/lists/show`

        Parameters
        ----------
        for_public : bool, optional
            Whether to show the user list for the public, by default False
        list_id : str, optional
            The id of the user list to show, by default None

        Returns
        -------
        UserList
            The user list
        """
        list_id = list_id or self.__list_id

        return await super().show(for_public=for_public, list_id=list_id)

    @override
    async def favorite(self, *, list_id: str | None = None) -> bool:
        """Favorite a user list

        Endpoint `/api/users/lists/favorite`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to favorite, by default None

        Returns
        -------
        bool
            True if the user list was favorited, False otherwise
        """
        list_id = list_id or self.__list_id

        return await super().favorite(list_id=list_id)

    @override
    async def unfavorite(self, *, list_id: str | None = None) -> bool:
        """Unfavorite a user list

        Endpoint `/api/users/lists/unfavorite`

        Parameters
        ----------
        list_id : str, optional
            The id of the user list to unfavorite, by default None

        Returns
        -------
        bool
            True if the user list was unfavorited, False otherwise
        """
        list_id = list_id or self.__list_id

        return await super().unfavorite(list_id=list_id)

    @override
    async def update(
        self, name: str = MISSING, is_public: bool = MISSING, *, list_id: str | None = None
    ) -> UserList:
        """Update a user list

        Endpoint `/api/users/lists/update`

        Parameters
        ----------
        name : str, optional
            The new name of the user list, by default MISSING
        is_public : bool, optional
            Whether the user list should be public, by default MISSING
        list_id : str, optional
            The id of the user list to update, by default None

        Returns
        -------
        UserList
            The updated user list
        """
        list_id = list_id or self.__list_id

        return await super().update(name=name, is_public=is_public, list_id=list_id)

    @override
    async def create_from_public(self, name: str, *, list_id: str | None = None):
        list_id = list_id or self.__list_id

        return await super().create_from_public(name=name, list_id=list_id)

    @override
    async def get_memberships(
        self,
        for_public: bool = False,
        limit: int = 30,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        list_id: str | None = None,
    ) -> list[UserListMembership]:
        list_id = list_id or self.__list_id

        return await super().get_memberships(
            for_public=for_public,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            list_id=list_id,
        )

    @override
    async def get_all_memberships(
        self,
        for_public: bool = False,
        limit: int = 30,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        list_id: str | None = None,
    ):
        list_id = list_id or self.__list_id

        async for i in super().get_all_memberships(
            for_public=for_public,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            list_id=list_id,
        ):
            yield i

    # ここからはusers/lists系じゃないが、ここにあってほしい物
    @override
    async def get_time_line(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
        *,
        list_id: str | None = None,
    ) -> list[Note]:
        list_id = list_id or self.__list_id

        return await super().get_time_line(
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            include_renote_my_notes=include_renote_my_notes,
            include_local_renotes=include_local_renotes,
            with_renotes=with_renotes,
            with_files=with_files,
            list_id=list_id,
        )

    @override
    async def get_all_time_line(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
        *,
        list_id: str | None = None,
    ):
        list_id = list_id or self.__list_id

        async for i in super().get_all_time_line(
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            include_renote_my_notes=include_renote_my_notes,
            include_local_renotes=include_local_renotes,
            with_renotes=with_renotes,
            with_files=with_files,
            list_id=list_id,
        ):
            yield i


class UserListActions(SharedUserListActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(self, name: str) -> UserList:
        """Create a new user list

        Endpoint `/api/users/lists/create`

        Parameters
        ----------
        name : str
            The name of the new user list

        Returns
        -------
        UserList
            The created user list
        """
        raw_user_list: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/create"), json={"name": name}, auth=True
        )
        return UserList(raw_user_list=raw_user_list, client=self._client)
