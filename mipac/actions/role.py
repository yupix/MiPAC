from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.config import config
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.models.roles import MeRole, Role, RoleUser
from mipac.types.note import INote
from mipac.types.roles import IMeRole, IRole, IRoleUser, is_me_role
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class RoleActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_list(self) -> list[Role]:
        res: list[IRole] = await self.__session.request(
            Route("POST", "/api/roles/list"), auth=True
        )

        return [Role(raw_role, client=self.__client) for raw_role in res]

    async def get(self, role_id: str) -> Role:
        """Get a role from the API.

        Parameters
        ----------
        role_id : str
            The ID of the role to get.

        Returns
        -------
        Role
            The role data.

        Raises
        ------
        NotSupportVersion
            If the version of the Misskey is less than 13.
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
    ) -> AsyncGenerator[MeRole | RoleUser, None]:
        if limit > 100:
            raise ValueError("Limit cannot be greater than 100")

        if get_all:
            limit = 100

        body = {"roleId": role_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IRoleUser | IMeRole](
            self.__session, Route("POST", "/api/roles/users"), auth=True, json=body
        )
        while True:
            raw_users = await pagination.next()
            for raw_user in raw_users:
                yield (
                    MeRole(raw_user, client=self.__client)
                    if is_me_role(raw_user, config.account_id)
                    else RoleUser(raw_user, client=self.__client)
                )

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
