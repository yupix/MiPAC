
from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.roles import Role
from mipac.types.roles import IRole

if TYPE_CHECKING:
    from mipac.client import ClientManager


class RoleActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_role(self, role_id: str) -> Role:
        """Get a role from the API.

        Parameters
        ----------
        role_id : str
            The ID of the role to get.

        Returns
        -------
        Role
            The role data.
        """
        
        raw_role: IRole = await self.__session.request(Route("POST", "/api/roles/show"), auth=True, json={"roleId":    role_id})
        return Role(raw_role, client=self.__client)
        