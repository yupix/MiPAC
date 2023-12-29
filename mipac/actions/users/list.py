from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.models.user import UserList
from mipac.types.user import IUserList
from mipac.utils.format import remove_dict_missing
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientPartialUserListActions(AbstractAction):
    """ユーザー向けのリストのアクションを提供します。"""

    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__user_id: str | None = user_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

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

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        raw_user_lists: list[IUserList] = await self._session.request(
            Route("POST", "/api/users/lists/list"), json={"userId": user_id}, auth=True
        )

        return [UserList(raw_user_list, client=self._client) for raw_user_list in raw_user_lists]

    async def pull(self, list_id: str, *, user_id: str | None = None) -> bool:
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

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/pull"),
            json={"listId": list_id, "userId": user_id},
            auth=True,
        )
        return res

    async def push(self, list_id: str, *, user_id: str | None = None) -> bool:
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

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/push"),
            json={"listId": list_id, "userId": user_id},
            auth=True,
        )
        return res

    async def update_member_ship(
        self, list_id: str, with_replies: bool = MISSING, *, user_id: str | None = None
    ):
        user_id = user_id or self.__user_id

        if user_id is None:
            raise ParameterError("required parameter user_id is missing")

        data = remove_dict_missing(
            {"listId": list_id, "userId": user_id, "withReplies": with_replies}
        )

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/update-membership"),
            json=data,
            auth=True,
        )
        return res


class ClientUserListActions(ClientPartialUserListActions):
    def __init__(
        self,
        list_id: str | None = None,
        *,
        user_id: str | None = None,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(user_id=user_id, session=session, client=client)
        self.__list_id: str | None = list_id

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

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/delete"), json={"listId": list_id}, auth=True
        )
        return res

    @override
    async def get_list(self, user_id: str) -> list[UserList]:
        return await super().get_list(user_id=user_id)

    @override
    async def pull(self, user_id: str, *, list_id: str | None = None) -> bool:
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        return await super().pull(list_id=list_id, user_id=user_id)

    @override
    async def push(self, user_id: str, *, list_id: str | None = None) -> bool:
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        return await super().push(list_id=list_id, user_id=user_id)

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

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        raw_user_list: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/show"),
            json={"listId": list_id, "forPublic": for_public},
            auth=True,
        )
        return UserList(raw_user_list=raw_user_list, client=self._client)

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
        list_id = list_id or self.__list_id

        res: bool = await self._session.request(
            Route("POST", "/api/users/lists/unfavorite"), json={"listId": list_id}, auth=True
        )
        return res

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

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        data = remove_dict_missing({"listId": list_id, "name": name, "public": is_public})

        res: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/update"),
            json=data,
            auth=True,
        )
        return UserList(raw_user_list=res, client=self._client)

    async def create_from_public(self, name: str, *, list_id: str | None = None):
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

        res: IUserList = await self._session.request(
            Route("POST", "/api/users/lists/create-from-public"),
            json={"listId": list_id, "name": name},
            auth=True,
        )
        return UserList(raw_user_list=res, client=self._client)

    async def update_member_ship(
        self, user_id: str, with_replies: bool = MISSING, list_id: str | None = None
    ):
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")
        return await super().update_member_ship(
            user_id=user_id, with_replies=with_replies, list_id=list_id
        )

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
        list_id: str | None = None,
    ) -> list[Note]:
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

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
        list_id: str | None = None,
    ):
        list_id = list_id or self.__list_id

        if list_id is None:
            raise ParameterError("required parameter list_id is missing")

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


class UserListActions(ClientUserListActions):
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

    @override
    async def delete(self, list_id: str) -> bool:
        return await super().delete(list_id=list_id)

    @override
    async def pull(self, list_id: str, user_id: str) -> bool:
        return await super().pull(list_id=list_id, user_id=user_id)

    @override
    async def push(self, list_id: str, user_id: str) -> bool:
        return await super().push(list_id=list_id, user_id=user_id)

    @override
    async def show(self, list_id: str, for_public: bool = False) -> UserList:
        return await super().show(list_id=list_id, for_public=for_public)

    @override
    async def favorite(self, list_id: str) -> bool:
        return await super().favorite(list_id=list_id)

    @override
    async def unfavorite(self, list_id: str) -> bool:
        return await super().unfavorite(list_id=list_id)

    @override
    async def update(
        self, list_id: str, name: str = MISSING, is_public: bool = MISSING
    ) -> UserList:
        return await super().update(name=name, is_public=is_public, list_id=list_id)

    @override
    async def create_from_public(self, list_id: str, name: str):
        return await super().create_from_public(name=name, list_id=list_id)

    @override
    async def update_member_ship(self, list_id: str, user_id: str, with_replies: bool = MISSING):
        return await super().update_member_ship(
            list_id=list_id, user_id=user_id, with_replies=with_replies
        )

    @override
    async def get_time_line(
        self,
        list_id: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
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

    @override
    async def get_all_time_line(
        self,
        list_id: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
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
