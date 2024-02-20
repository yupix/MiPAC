from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.invite import ClientInviteActions, InviteActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientInviteManager(AbstractManager):
    def __init__(self, invite_id: str, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__actions: ClientInviteActions = ClientInviteActions(
            invite_id=invite_id, session=session, client=client
        )

    @property
    def action(self) -> ClientInviteActions:
        return self.__actions


class InviteManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__actions: InviteActions = InviteActions(session=session, client=client)

    @property
    def action(self) -> InviteActions:
        return self.__actions
