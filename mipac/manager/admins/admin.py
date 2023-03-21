from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.admin import AdminActions
from mipac.http import HTTPClient
from mipac.manager.admins.ad import AdminAdvertisingManager, AdminAdvertisingModelManager
from mipac.manager.admins.announcement import AdminAnnouncementManager
from mipac.manager.admins.emoji import AdminEmojiManager
from mipac.manager.admins.moderator import AdminModeratorManager
from mipac.manager.admins.roles import AdminRolesManager, AdminRolesModelManager
from mipac.manager.admins.user import AdminUserManager

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AdminManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.emoji: AdminEmojiManager = AdminEmojiManager(session=session, client=client)
        self.user: AdminUserManager = AdminUserManager(session=session, client=client)
        self.ad: AdminAdvertisingManager = AdminAdvertisingManager(session=session, client=client)
        self.moderator: AdminModeratorManager = AdminModeratorManager(
            session=session, client=client
        )
        self.announcement: AdminAnnouncementManager = AdminAnnouncementManager(
            session=session, client=client
        )
        self.role: AdminRolesManager = AdminRolesManager(session=session, client=client)

    @property
    def action(self) -> AdminActions:
        return AdminActions(session=self.__session, client=self.__client)

    def create_roles_model_manager(self, role_id: str | None = None) -> AdminRolesModelManager:
        return AdminRolesModelManager(
            role_id=role_id, session=self.__session, client=self.__client
        )

    def create_ad_model_manager(self, ad_id: str | None = None) -> AdminAdvertisingModelManager:
        return AdminAdvertisingModelManager(
            ad_id=ad_id, session=self.__session, client=self.__client
        )
