from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.announcement import AdminAnnouncementActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminAnnouncementManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminAnnouncementActions:
        return AdminAnnouncementActions(
            session=self.__session, client=self.__client
        )

    def _create_admin_announcement_instance(
        self, announce_id: str
    ) -> AdminAnnouncementActions:
        return AdminAnnouncementActions(
            announce_id=announce_id,
            session=self.__session,
            client=self.__client,
        )
