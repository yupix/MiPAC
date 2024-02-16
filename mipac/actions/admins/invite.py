from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.invite import InviteCode
from mipac.types.invite import IInviteCode
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminInviteActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def create_invite(
        self, count: int = 1, expires_at: str | None = None
    ) -> list[InviteCode]:
        raw_codes: list[IInviteCode] = await self.__session.request(
            route=Route(method="POST", path="/api/admin/invite/create"),
            json={"count": count, "expiresAt": expires_at},
            auth=True,
        )
        return [InviteCode(raw_code, client=self.__client) for raw_code in raw_codes]

    async def get_invite_list(
        self,
        limit: int = 30,
        offset: int = 0,
        type: Literal["unused", "used", "expired", "all"] = "all",
        sort: Literal["+createdAt", "-createdAt", "+usedAt", "-usedAt"] = "+createdAt",
    ) -> list[InviteCode]:
        body = remove_dict_empty(
            {
                "limit": limit,
                "offset": offset,
                "type": type,
                "sort": sort,
            }
        )

        res: list[IInviteCode] = await self._session.request(
            Route("POST", "/api/admin/invite/list"), json=body, auth=True
        )

        return [InviteCode(raw_invite_code, client=self.__client) for raw_invite_code in res]

    async def get_all_invite_list(
        self,
        limit: int = 30,
        offset: int = 0,
        type: Literal["unused", "used", "expired", "all"] = "all",
        sort: Literal["+createdAt", "-createdAt", "+usedAt", "-usedAt"] = "+createdAt",
    ):
        body = remove_dict_empty(
            {
                "limit": limit,
                "offset": offset,
                "type": type,
                "sort": sort,
            }
        )

        pagination = Pagination[IInviteCode](
            http_client=self.__session,
            route=Route("POST", "/api/admin/invite/list"),
            json=body,
            pagination_type="count",
            auth=True,
        )
        while pagination.is_final is False:
            raw_invite_codes = await pagination.next()
            for raw_invite_code in raw_invite_codes:
                yield InviteCode(raw_invite_code, client=self.__client)
