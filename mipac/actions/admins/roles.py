from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion, NotSupportVersionText
from mipac.http import Route
from mipac.models.roles import Role
from mipac.types.roles import IRole

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class AdminRoleActions(AbstractAction):
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__role_id: str | None = role_id

    async def create(
        self,
        name: str,
        description: str,
        color: str | None = None,
        iconUrl: str| None = None,
        target: Literal['manual', 'conditional'] = 'manual',
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        policies: dict[Any, Any] | None = None,
    ) -> Role:
        body = {
            'name': name,
            'description': description,
            'color': color,
            'iconUrl': iconUrl,
            'target': target,
            'condFormula': cond_formula or {},
            'isPublic': is_public,
            'isModerator': is_moderator,
            'isAdministrator': is_administrator,
            'asBadge': as_badge,
            'canEditMembersByModerator': can_edit_members_by_moderator,
            'policies': policies or {},
        }
        if self.__client._config.use_version >= 13:
            res: IRole = await self.__session.request(
                Route('POST', '/api/admin/roles/create'),
                auth=True, json=body, lower=True, remove_none=False
            )
            return Role(res)
        raise NotSupportVersion(NotSupportVersionText)


    async def show(self, role_id: str) -> Role:
        if self.__client._config.use_version >= 13:
            res: IRole = await self.__session.request(
                Route('POST', '/api/admin/roles/show'),
                json={'roleId': role_id},
                auth=True,
                lower=True,
            )
            return Role(res)
        raise NotSupportVersion(NotSupportVersionText)

    async def assign(self, role_id: str, user_id: str, expires_at: int | None = None) -> bool:
        """指定したユーザーに指定したロールを付与します

        Parameters
        ----------
        role_id : str
            ロールのID
        user_id : str
            ロールを付与する対象のユーザーID
        expires_at : int | None, optional
            いつまでロールを付与するか, by default None

        Returns
        -------
        bool
            成功したか否か
        """
        body = {'roleId': role_id, 'userId': user_id, 'expiresAt': expires_at}
        res: bool = await self.__session.request(
            Route('POST', '/api/admin/roles/assign'), auth=True, json=body
        )
        return res
