from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.admin import AdminActions
from mipac.http import HTTPClient
from mipac.manager.ad import AdminAdvertisingManager
from mipac.manager.admins.emoji import AdminEmojiManager
from mipac.manager.admins.moderator import AdminModeratorManager
from mipac.manager.admins.user import AdminUserManager

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.emoji = AdminEmojiManager(session=session, client=client)
        self.user = AdminUserManager(session=session, client=client)
        self.ad = AdminAdvertisingManager(session=session, client=client)
        self.moderator = AdminModeratorManager(session=session, client=client)

    @property
    def action(self) -> AdminActions:
        return AdminActions(session=self.__session, client=self.__client)
