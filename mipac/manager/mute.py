from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.mute import MuteActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MuteManager(AbstractManager):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ) -> None:
        self._user_id: str | None = user_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @property
    def action(self) -> MuteActions:
        return MuteActions(
            user_id=self._user_id, session=self._session, client=self._client
        )
