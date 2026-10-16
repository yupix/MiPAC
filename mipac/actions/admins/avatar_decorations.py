from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.avatar_decoration import AvatarDecoration
from mipac.types.avatar_decoration import IAvatarDecoration
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedAvatarDecorationActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, avatar_decoration_id: str) -> bool:
        res: bool = await self._session.request(
            Route("POST", "/api/admin/avatar-decorations/delete"),
            json={"id": avatar_decoration_id},
        )
        return res

    async def update(
        self,
        name: str = MISSING,
        description: str = MISSING,
        url: str = MISSING,
        category: str | None = MISSING,
        role_ids_that_can_be_used_this_decoration: list[str] = MISSING,
        *,
        avatar_decoration_id: str,
    ) -> AvatarDecoration:
        body = remove_dict_missing(
            {
                "id": avatar_decoration_id,
                "name": name,
                "description": description,
                "url": url,
                "category": category,
                "roleIdsThatCanBeUsedThisDecoration": role_ids_that_can_be_used_this_decoration,
            }
        )

        raw_avatar_decoration: IAvatarDecoration = await self._session.request(
            Route("POST", "/api/admin/avatar-decorations/update"), json=body
        )

        return AvatarDecoration(raw_avatar_decoration, client=self._client)


class AdminAvatarDecorationActions(SharedAvatarDecorationActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        name: str,
        description: str,
        url: str,
        category: str | None = None,
        role_ids_that_can_be_used_this_decoration: list[str] = MISSING,
    ) -> AvatarDecoration:
        body = remove_dict_missing(
            {
                "name": name,
                "description": description,
                "url": url,
                "category": category,
                "roleIdsThatCanBeUsedThisDecoration": role_ids_that_can_be_used_this_decoration,
            }
        )

        raw_avatar_decoration: IAvatarDecoration = await self._session.request(
            Route("POST", "/api/admin/avatar-decorations/create"), json=body
        )

        return AvatarDecoration(raw_avatar_decoration, client=self._client)

    async def get_list(
        self,
        limit: int = MISSING,
        since_id: str = MISSING,
        until_id: str = MISSING,
        user_id: str | None = None,
    ) -> list[AvatarDecoration]:
        body = remove_dict_missing(
            {"limit": limit, "sinceId": since_id, "untilId": until_id, "userId": user_id}
        )

        raw_avatar_decorations: list[IAvatarDecoration] = await self._session.request(
            Route("POST", "/api/admin/avatar-decorations/list"), json=body
        )

        return [
            AvatarDecoration(raw_avatar_decoration, client=self._client)
            for raw_avatar_decoration in raw_avatar_decorations
        ]

    async def get_all_list(
        self,
        limit: int = MISSING,
        since_id: str = MISSING,
        until_id: str = MISSING,
        user_id: str | None = None,
    ):
        body = remove_dict_missing(
            {"limit": limit, "sinceId": since_id, "untilId": until_id, "userId": user_id}
        )
        pagination = Pagination[IAvatarDecoration](
            http_client=self._session,
            route=Route("POST", "/api/admin/avatar-decorations/list"),
            json=body,
        )

        while pagination.is_final is False:
            raw_avatar_decorations: list[IAvatarDecoration] = await pagination.next()
            for raw_avatar_decoration in raw_avatar_decorations:
                yield AvatarDecoration(raw_avatar_decoration, client=self._client)


class ClientAdminAvatarDecorationActions(AbstractAction):
    def __init__(self, avatar_decoration_id: str, *, session: HTTPClient, client: ClientManager):
        self.__actions: SharedAvatarDecorationActions = SharedAvatarDecorationActions(
            session=session, client=client
        )
        self.__avatar_decoration_id: str = avatar_decoration_id

    async def delete(self, *, avatar_decoration_id: str = MISSING) -> bool:
        avatar_decoration_id = avatar_decoration_id or self.__avatar_decoration_id

        return await self.__actions.delete(avatar_decoration_id=avatar_decoration_id)

    async def update(
        self,
        name: str = MISSING,
        description: str = MISSING,
        url: str = MISSING,
        category: str | None = MISSING,
        role_ids_that_can_be_used_this_decoration: list[str] = MISSING,
        *,
        avatar_decoration_id: str = MISSING,
    ) -> AvatarDecoration:
        avatar_decoration_id = avatar_decoration_id or self.__avatar_decoration_id

        return await self.__actions.update(
            name=name,
            description=description,
            url=url,
            category=category,
            role_ids_that_can_be_used_this_decoration=role_ids_that_can_be_used_this_decoration,
            avatar_decoration_id=avatar_decoration_id,
        )
