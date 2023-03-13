from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Literal

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion, NotSupportVersionText, ParameterError
from mipac.http import Route
from mipac.models.roles import Role, RoleUser
from mipac.types.meta import IPolicies
from mipac.types.roles import IRole, IRoleUser

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class AdminRoleModelActions(AbstractAction):
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client
        self._role_id: str | None = role_id

    async def update(
        self,
        name: str,
        description: str,
        role_id: str | None = None,
        color: str | None = None,
        iconUrl: str | None = None,
        target: Literal['manual', 'conditional'] = 'manual',
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        policies: dict[Any, Any] | None = None,
    ) -> bool:
        if self._client._config.use_version >= 13:
            role_id = self._role_id or role_id
            if role_id is None:
                raise ParameterError('role_idは必須です')
            body = {
                'roleId': role_id,
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
            res: bool = await self._session.request(
                Route('POST', '/api/admin/roles/update'),
                json=body,
                auth=True,
                lower=True,
                remove_none=False,
            )
            return res
        raise NotSupportVersion(NotSupportVersionText)

    async def delete(self, role_id: str | None = None) -> bool:
        if self._client._config.use_version >= 13:
            role_id = self._role_id or role_id
            if role_id is None:
                raise ParameterError('role_idは必須です')
            res: bool = await self._session.request(
                Route('POST', '/api/admin/roles/delete'),
                auth=True,
                json={'roleId': role_id},
                lower=True,
            )
            return res
        raise NotSupportVersion(NotSupportVersionText)

    async def assign(
        self, user_id: str, role_id: str | None = None, expires_at: int | None = None
    ) -> bool:
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
        if self._client._config.use_version >= 13:
            if role_id is None:
                raise ParameterError('role_idは必須です')
            body = {'roleId': role_id, 'userId': user_id, 'expiresAt': expires_at}
            res: bool = await self._session.request(
                Route('POST', '/api/admin/roles/assign'), auth=True, json=body
            )
            return res
        raise NotSupportVersion(NotSupportVersionText)

    async def unassign(self, user_id: str, role_id: str | None = None) -> bool:
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
        if self._client._config.use_version >= 13:
            role_id = self._role_id or role_id
            if role_id is None:
                raise ParameterError('role_idは必須です')
            body = {'roleId': role_id, 'userId': user_id}
            res: bool = await self._session.request(
                Route('POST', '/api/admin/roles/unassign'), auth=True, json=body
            )
            return res
        raise NotSupportVersion(NotSupportVersionText)

    async def show(self, role_id: str | None = None) -> Role:
        if self._client._config.use_version >= 13:
            role_id = self._role_id or role_id
            if role_id is None:
                raise ParameterError('role_idは必須です')
            res: IRole = await self._session.request(
                Route('POST', '/api/admin/roles/show'),
                json={'roleId': role_id},
                auth=True,
                lower=True,
            )
            return Role(res, client=self._client)
        raise NotSupportVersion(NotSupportVersionText)

    async def get_users(
        self,
        role_id: str | None = None,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 100,
        all: bool = False,
    ) -> AsyncGenerator[RoleUser, None]:
        if self._client._config.use_version < 13:
            raise NotSupportVersion(NotSupportVersionText)
        role_id = self._role_id or role_id
        if role_id is None:
            raise ParameterError('role_idは必須です')

        async def request(body) -> list[RoleUser]:
            res: list[IRoleUser] = await self._session.request(
                Route('POST', '/api/admin/roles/users'), lower=True, auth=True, json=body,
            )
            return [RoleUser(role, client=self._client) for role in res]

        data = {'limit': limit, 'sinceId': since_id, 'untilId': until_id, 'roleId': role_id}
        if all:
            data['limit'] = 100
        first_req = await request(data)
        for user in first_req:
            yield user

        if all and len(first_req) == 100:
            data['untilId'] = first_req[-1].id
            while True:
                res = await request(data)
                if len(res) <= 100:
                    for user in res:
                        yield user
                if len(res) == 0:
                    break
                data['untilId'] = res[-1].id


class AdminRoleActions(AdminRoleModelActions):
    def __init__(self, role_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        super().__init__(role_id=role_id, session=session, client=client)

    async def create(
        self,
        name: str,
        description: str,
        color: str | None = None,
        iconUrl: str | None = None,
        target: Literal['manual', 'conditional'] = 'manual',
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        policies: dict[Any, Any] | None = None,
    ) -> Role:
        if self._client._config.use_version >= 13:
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
            res: IRole = await self._session.request(
                Route('POST', '/api/admin/roles/create'),
                auth=True,
                json=body,
                lower=True,
                remove_none=False,
            )
            return Role(res, client=self._client)
        raise NotSupportVersion(NotSupportVersionText)

    async def get_list(self) -> list[Role]:
        if self._client._config.use_version >= 13:
            res: list[IRole] = await self._session.request(
                Route('POST', '/api/admin/roles/list'), auth=True, lower=True
            )
            return [Role(i, client=self._client) for i in res]
        raise NotSupportVersion(NotSupportVersionText)

    async def update_default_policies(self, policies: IPolicies):
        if self._client._config.use_version >= 13:
            body = {
                'policies': {
                    'gtlAvailable': policies.get('gtl_available'),
                    'ltlAvailable': policies.get('ltl_available'),
                    'canPublicNote': policies.get('can_public_note'),
                    'canInvite': policies.get('can_invite'),
                    'canManageCustomEmojis': policies.get('can_manage_custom_emojis'),
                    'canHideAds': policies.get('can_hide_ads'),
                    'driveCapacityMb': policies.get('drive_capacity_mb'),
                    'pinLimit': policies.get('pin_limit'),
                    'antennaLimit': policies.get('antenna_limit'),
                    'wordMuteLimit': policies.get('word_mute_limit'),
                    'webhookLimit': policies.get('webhook_limit'),
                    'clipLimit': policies.get('clip_limit'),
                    'noteEachClipsLimit': policies.get('note_each_clips_limit'),
                    'userListLimit': policies.get('user_list_limit'),
                    'userEachUserListsLimit': policies.get('user_each_user_lists_limit'),
                    'rateLimitFactor': policies.get('rate_limit_factor'),
                }
            }
            res = await self._session.request(
                Route('POST', '/api/admin/roles/update-default-policies'),
                auth=True,
                lower=True,
                json=body,
            )
            return res
        raise NotSupportVersion(NotSupportVersionText)
