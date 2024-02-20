from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.users.mute import ClientMuteActions, MuteActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientMuteManager(AbstractManager):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        self._action: ClientMuteActions = ClientMuteActions(
            user_id=user_id, session=session, client=client
        )

    @property
    def action(self) -> ClientMuteActions:
        return self._action


class MuteManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._action: MuteActions = MuteActions(session=session, client=client)

    @property
    def action(self) -> MuteActions:
        return self._action
