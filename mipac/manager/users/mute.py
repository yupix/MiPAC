
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.users.mute import MuteActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MuteManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> MuteActions:
        return MuteActions(session=self.__session, client=self.__client)
