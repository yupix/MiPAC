from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.invite import InviteCode, InviteLimit
from mipac.types.invite import IInviteCode, IInviteLimit
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedInviteActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, invite_id: str) -> bool:
        """Delete an invite code.

        Parameters
        ----------
        invite_id : str | None, optional
            The invite code to delete, by default None

        Returns
        -------
        bool
            Whether the invite code was deleted.
        """

        res: bool = await self._session.request(
            Route("POST", "/api/invite/delete"), json={"inviteId": invite_id}, auth=True
        )

        return res


class ClientInviteActions(SharedInviteActions):
    def __init__(self, invite_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self._invite_id: str = invite_id

    @override
    async def delete(self, *, invite_id: str | None = None) -> bool:
        """Delete an invite code.

        Parameters
        ----------
        invite_id : str | None, optional
            The invite code to delete, by default None

        Returns
        -------
        bool
            Whether the invite code was deleted.
        """

        invite_id = invite_id or self._invite_id

        return await super().delete(invite_id=invite_id)


class InviteActions(SharedInviteActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(self) -> InviteCode:
        """Create a new invite code.

        Endpoint: `/api/invite/create`

        Returns
        -------
        PartialInviteCode
            The invite code created.
        """
        raw_code: IInviteCode = await self._session.request(
            Route("POST", "/api/invite/create"), auth=True
        )
        return InviteCode(raw_code, client=self._client)

    async def get_list(
        self, limit: int = 30, since_id: str | None = None, until_id: str | None = None
    ) -> list[InviteCode]:
        """Get a list of invitation codes created by you.

        Endpoint: `/api/invite/list`

        Parameters
        ----------
        limit : int, optional
            The number of invite codes to get, by default 30
        since_id : str | None, optional
            The id of the invite code to get since, by default None
        until_id : str | None, optional
            The id of the invite code to get until, by default None

        Returns
        -------
        list[PartialInviteCode]
            The list of invite codes.
        """

        data = {"limit": limit, "sinceId": since_id, "untilId": until_id}

        raw_codes: list[IInviteCode] = await self._session.request(
            Route("POST", "/api/invite/list"), auth=True, json=data
        )
        return [InviteCode(raw_code, client=self._client) for raw_code in raw_codes]

    async def get_all_list(
        self, since_id: str | None = None, until_id: str | None = None
    ) -> AsyncGenerator[InviteCode, None]:
        """Get all invite codes created by you.

        Endpoint: `/api/invite/list`

        Parameters
        ----------
        since_id : str | None, optional
            The id of the invite code to get since, by default None
        until_id : str | None, optional
            The id of the invite code to get until, by default None

        Returns
        -------
        list[PartialInviteCode]
            The list of invite codes.
        """

        data = {"limit": 100, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IInviteCode](
            self._session, Route("POST", "/api/invite/list"), auth=True, json=data
        )
        while pagination.is_final is False:
            raw_codes: list[IInviteCode] = await pagination.next()
            for raw_code in raw_codes:
                yield InviteCode(raw_code, client=self._client)

    async def get_limit(self) -> InviteLimit:
        """Get the number of invite codes you can create.

        Endpoint: `/api/invite/limit`

        Returns
        -------
        int
            The number of invite codes you can create.
        """

        raw_invite_limit: IInviteLimit = await self._session.request(
            Route("POST", "/api/invite/limit"), auth=True
        )
        return InviteLimit(raw_invite_limit, client=self._client)
