from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.invite import InviteCode
from mipac.types.invite import IInviteCode

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientInviteActions(AbstractAction):
    def __init__(self, invite_id: str | None, *, session: HTTPClient, client: ClientManager):
        self._invite_id: str | None = invite_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

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

        res: bool = await self._session.request(
            Route("POST", "/api/invite/delete"), json={"inviteId": invite_id}, auth=True
        )

        return res


class InviteActions(ClientInviteActions):
    def __init__(
        self, invite_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        super().__init__(invite_id=invite_id, session=session, client=client)

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

    async def delete(self, invite_id: str) -> bool:
        """Delete an invite code.

        Endpoint: `/api/invite/delete`

        Parameters
        ----------
        invite_id : str
            The invite code to delete

        Returns
        -------
        bool
            Whether the invite code was deleted.
        """

        return await super().delete(invite_id=invite_id)
