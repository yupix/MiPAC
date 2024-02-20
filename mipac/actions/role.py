from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.models.roles import Role, RoleUser
from mipac.types.note import INote
from mipac.types.roles import IRole, IRoleUser
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class RoleActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_list(self) -> list[Role]:
        """
        Get a list of roles from the API.
        Endpoint: `/api/roles/list`

        Returns
        -------
        list[Role]
            The role data.
        """
        res: list[IRole] = await self.__session.request(
            Route("POST", "/api/roles/list"), auth=True
        )

        return [Role(raw_role, client=self.__client) for raw_role in res]

    async def get(self, role_id: str) -> Role:
        """
        Get a role from the API.
        Endpoint: `/api/roles/show`

        Parameters
        ----------
        role_id : str
            The ID of the role to get.

        Returns
        -------
        Role
            The role data.
        """
        raw_role: IRole = await self.__session.request(
            Route("POST", "/api/roles/show"), auth=True, json={"roleId": role_id}
        )
        return Role(raw_role, client=self.__client)

    async def get_users(
        self,
        role_id: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[RoleUser, None]:
        """
        Get users in a role.
        Endpoint: `/api/roles/users`

        Parameters
        ----------
        role_id : str
            The ID of the role to get users.
        since_id : str, optional
            The ID of the user to get users after, by default None
        until_id : str, optional
            The ID of the user to get users before, by default None
        limit : int, optional
            The number of users to get, by default 10
        get_all : bool, optional
            Whether to get all users, by default False

        Yields
        ------
        AsyncGenerator[RoleUser, None]
            The role user data.
        """

        if limit > 100:
            raise ValueError("Limit cannot be greater than 100")

        if get_all:
            limit = 100

        body = {"roleId": role_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IRoleUser](
            self.__session, Route("POST", "/api/roles/users"), auth=True, json=body
        )
        while True:
            raw_users = await pagination.next()
            for raw_user in raw_users:
                yield RoleUser(raw_user, client=self.__client)

            if pagination.is_final or get_all is False:
                break

    async def get_notes(
        self,
        role_id: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        *,
        get_all: bool = False,
    ):
        """
        Get notes in a role.
        Endpoint: `/api/roles/notes`

        Parameters
        ----------
        role_id : str
            The ID of the role to get notes.
        limit : int, optional
            The number of notes to get, by default 10
        since_id : str, optional
            The ID of the note to get notes after, by default None
        until_id : str, optional
            The ID of the note to get notes before, by default None
        since_data : int, optional
            The timestamp of the note to get notes after, by default None
        until_data : int, optional
            The timestamp of the note to get notes before, by default None
        get_all : bool, optional
            Whether to get all notes, by default False

        Yields
        ------
        AsyncGenerator[Note, None]
            The note data.
        """

        if limit > 100:
            raise ValueError("Limit cannot be greater than 100")

        if get_all:
            limit = 100

        body = {
            "roleId": role_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceData": since_data,
            "untilData": until_data,
        }

        pagination = Pagination[INote](
            self.__session, Route("POST", "/api/roles/notes"), auth=True, json=body
        )
        while True:
            raw_notes = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note, client=self.__client)

            if pagination.is_final or get_all is False:
                break
