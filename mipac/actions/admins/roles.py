from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, override

from mipac.http import HTTPClient, Route
from mipac.models.roles import Role, RoleUser
from mipac.types.meta import IPolicies
from mipac.types.roles import IRole, IRoleUser
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class SharedAdminRoleActions:
    def __init__(self, *, session: HTTPClient, client: ClientManager) -> None:
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, role_id: str) -> bool:
        res: bool = await self._session.request(
            Route("POST", "/api/admin/roles/delete"),
            json={"roleId": role_id},
        )
        return res

    async def update(
        self,
        name: str,
        description: str,
        color: str | None = None,
        iconUrl: str | None = None,
        target: Literal["manual", "conditional"] = "manual",
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        is_explorable: bool = MISSING,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        display_order: int = 0,
        policies: dict[Any, Any] | None = None,
        *,
        role_id: str,
    ) -> bool:
        body = remove_dict_missing(
            {
                "roleId": role_id,
                "name": name,
                "description": description,
                "color": color,
                "iconUrl": iconUrl,
                "target": target,
                "condFormula": cond_formula or {},
                "isPublic": is_public,
                "isModerator": is_moderator,
                "isAdministrator": is_administrator,
                "isExplorable": is_explorable,
                "asBadge": as_badge,
                "canEditMembersByModerator": can_edit_members_by_moderator,
                "displayOrder": display_order,
                "policies": policies or {},
            }
        )
        res: bool = await self._session.request(
            Route("POST", "/api/admin/roles/update"),
            json=body,
            remove_none=False,
        )
        return res

    async def assign(self, user_id: str, expires_at: int | None = None, *, role_id: str) -> bool:
        """指定したユーザーに指定したロールを付与します

        Parameters
        ----------
        user_id : str
            ロールを付与する対象のユーザーID
        expires_at : int | None, optional
            いつまでロールを付与するか, by default None
        role_id : str
            ロールのID

        Returns
        -------
        bool
            成功したか否か
        """
        body = {"roleId": role_id, "userId": user_id, "expiresAt": expires_at}
        res: bool = await self._session.request(
            Route("POST", "/api/admin/roles/assign"), auth=True, json=body
        )
        return res

    async def unassign(self, user_id: str, *, role_id: str) -> bool:
        """指定したユーザーから指定したロールを解除します

        Parameters
        ----------
        user_id : str
            ロールを解除するユーザーID
        role_id : str
            ロールのID

        Returns
        -------
        bool
            成功したか否か
        """
        body = {"roleId": role_id, "userId": user_id}
        res: bool = await self._session.request(
            Route("POST", "/api/admin/roles/unassign"), auth=True, json=body
        )
        return res

    async def get_users(
        self,
        since_id: str = MISSING,
        until_id: str = MISSING,
        limit: int = MISSING,
        *,
        role_id: str,
    ) -> RoleUser:
        body = remove_dict_missing(
            {"limit": limit, "sinceId": since_id, "untilId": until_id, "roleId": role_id}
        )

        raw_role_user: IRoleUser = await self._session.request(
            Route("POST", "/api/admin/roles/users"), json=body
        )

        return RoleUser(raw_role_user, client=self._client)

    async def get_all_users(
        self,
        since_id: str = MISSING,
        until_id: str = MISSING,
        limit: int = MISSING,
        *,
        role_id: str,
    ):
        """指定したロールを持つユーザーを全て取得します

        Parameters
        ----------
        since_id : str, optional
            ページネーションの開始位置, by default MISSING
        until_id : str, optional
            ページネーションの終了位置, by default MISSING
        limit : int, optional
            1ページあたりの取得数, by default MISSING
        role_id : str
            ロールのID

        Returns
        -------
        RoleUser
            ロールユーザー
        """
        body = remove_dict_missing(
            {"sinceId": since_id, "untilId": until_id, "limit": limit, "roleId": role_id}
        )

        pagination = Pagination[IRoleUser](
            self._session, Route("POST", "/api/admin/roles/users"), json=body
        )

        while pagination.is_final is False:
            raw_role_users = await pagination.next()
            for raw_role_user in raw_role_users:
                yield RoleUser(raw_role_user, client=self._client)


class ClientAdminRoleActions(SharedAdminRoleActions):
    def __init__(self, role_id: str, *, session: HTTPClient, client: ClientManager) -> None:
        super().__init__(session=session, client=client)
        self.__role_id: str = role_id

    @override
    async def delete(self, *, role_id: str | None = None) -> bool:
        role_id = role_id or self.__role_id

        if role_id is None:
            raise ValueError("required role_id")

        return await super().delete(role_id=role_id)

    @override
    async def update(
        self,
        name: str,
        description: str,
        color: str | None = None,
        iconUrl: str | None = None,
        target: Literal["manual"] | Literal["conditional"] = "manual",
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        is_explorable: bool = MISSING,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        display_order: int = 0,
        policies: dict[Any, Any] | None = None,
        *,
        role_id: str | None = None,
    ) -> bool:
        role_id = role_id or self.__role_id

        if role_id is None:
            raise ValueError("required role_id")

        return await super().update(
            name=name,
            description=description,
            color=color,
            iconUrl=iconUrl,
            target=target,
            cond_formula=cond_formula,
            is_public=is_public,
            is_moderator=is_moderator,
            is_administrator=is_administrator,
            is_explorable=is_explorable,
            as_badge=as_badge,
            can_edit_members_by_moderator=can_edit_members_by_moderator,
            display_order=display_order,
            policies=policies,
            role_id=role_id,
        )

    @override
    async def assign(
        self, user_id: str, expires_at: int | None = None, *, role_id: str | None = None
    ) -> bool:
        role_id = role_id or self.__role_id

        if role_id is None:
            raise ValueError("required role_id")

        return await super().assign(user_id=user_id, expires_at=expires_at, role_id=role_id)

    @override
    async def unassign(self, user_id: str, *, role_id: str | None = None) -> bool:
        role_id = role_id or self.__role_id

        if role_id is None:
            raise ValueError("required role_id")

        return await super().unassign(user_id=user_id, role_id=role_id)

    @override
    async def get_users(
        self,
        since_id: str = MISSING,
        until_id: str = MISSING,
        limit: int = MISSING,
        *,
        role_id: str,
    ) -> RoleUser:
        return await super().get_users(
            since_id=since_id, until_id=until_id, limit=limit, role_id=role_id
        )

    @override
    async def get_all_users(
        self,
        since_id: str = MISSING,
        until_id: str = MISSING,
        limit: int = MISSING,
        *,
        role_id: str,
    ):
        return super().get_all_users(
            since_id=since_id, until_id=until_id, limit=limit, role_id=role_id
        )


class AdminRoleActions(SharedAdminRoleActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        name: str,
        description: str,
        color: str | None = None,
        iconUrl: str | None = None,
        target: Literal["manual", "conditional"] = "manual",
        cond_formula: dict[Any, Any] | None = None,
        is_public: bool = False,
        is_moderator: bool = False,
        is_administrator: bool = False,
        is_explorable: bool = False,
        as_badge: bool = False,
        can_edit_members_by_moderator: bool = False,
        display_order: int = 0,
        policies: dict[Any, Any] | None = None,
    ) -> Role:
        body = {
            "name": name,
            "description": description,
            "color": color,
            "iconUrl": iconUrl,
            "target": target,
            "condFormula": cond_formula or {},
            "isPublic": is_public,
            "isModerator": is_moderator,
            "isAdministrator": is_administrator,
            "isExplorable": is_explorable,
            "asBadge": as_badge,
            "canEditMembersByModerator": can_edit_members_by_moderator,
            "displayOrder": display_order,
            "policies": policies or {},
        }
        res: IRole = await self._session.request(
            Route("POST", "/api/admin/roles/create"),
            auth=True,
            json=body,
            lower=True,
            remove_none=False,
        )
        return Role(res, client=self._client)

    async def get_list(self) -> list[Role]:
        res: list[IRole] = await self._session.request(
            Route("POST", "/api/admin/roles/list"), auth=True, lower=True
        )
        return [Role(i, client=self._client) for i in res]

    async def update_default_policies(self, policies: IPolicies):
        body = {
            "policies": {
                "gtlAvailable": policies.get("gtl_available"),
                "ltlAvailable": policies.get("ltl_available"),
                "canPublicNote": policies.get("can_public_note"),
                "canInvite": policies.get("can_invite"),
                "canManageCustomEmojis": policies.get("can_manage_custom_emojis"),
                "canHideAds": policies.get("can_hide_ads"),
                "driveCapacityMb": policies.get("drive_capacity_mb"),
                "pinLimit": policies.get("pin_limit"),
                "antennaLimit": policies.get("antenna_limit"),
                "wordMuteLimit": policies.get("word_mute_limit"),
                "webhookLimit": policies.get("webhook_limit"),
                "clipLimit": policies.get("clip_limit"),
                "noteEachClipsLimit": policies.get("note_each_clips_limit"),
                "userListLimit": policies.get("user_list_limit"),
                "userEachUserListsLimit": policies.get("user_each_user_lists_limit"),
                "rateLimitFactor": policies.get("rate_limit_factor"),
            }
        }
        res = await self._session.request(
            Route("POST", "/api/admin/roles/update-default-policies"),
            auth=True,
            lower=True,
            json=body,
        )
        return res
