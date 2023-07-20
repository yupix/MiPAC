from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.antenna import AntennaActions, ClientAntennaActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientAntennaManager(AbstractManager):
    def __init__(self, *, antenna_id: str, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__antenna_id: str = antenna_id

    @property
    def action(self) -> ClientAntennaActions:
        return ClientAntennaActions(
            antenna_id=self.__antenna_id, session=self.__session, client=self.__client
        )


class AntennaManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AntennaActions:
        return AntennaActions(session=self.__session, client=self.__client)

    def _create_client_antenna_manager(self, antenna_id: str) -> ClientAntennaManager:
        return ClientAntennaManager(
            antenna_id=antenna_id, session=self.__session, client=self.__client
        )
