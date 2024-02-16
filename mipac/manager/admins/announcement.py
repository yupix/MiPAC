from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.announcement import (
    AdminAnnouncementActions,
    ClientAdminAnnouncementActions,
)
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientAdminAnnouncementManager(AbstractManager):
    def __init__(self, announce_id: str, *, session: HTTPClient, client: ClientManager):
        self.__announce_id: str = announce_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ClientAdminAnnouncementActions:
        return ClientAdminAnnouncementActions(
            announce_id=self.__announce_id, session=self.__session, client=self.__client
        )


class AdminAnnouncementManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: AdminAnnouncementActions = AdminAnnouncementActions(
            session=self.__session, client=self.__client
        )

    @property
    def action(self) -> AdminAnnouncementActions:
        return self.__action
