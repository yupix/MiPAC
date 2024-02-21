from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.admin import AdminActions
from mipac.http import HTTPClient
from mipac.manager.admins.accounts import AdminAccountManager
from mipac.manager.admins.ad import AdminAdManager, ClientAdminAdManager
from mipac.manager.admins.announcement import (
    AdminAnnouncementManager,
    ClientAdminAnnouncementManager,
)
from mipac.manager.admins.drive import AdminDriveManager
from mipac.manager.admins.emoji import AdminEmojiManager
from mipac.manager.admins.invite import AdminInviteManager
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
        self.ad: AdminAdManager = AdminAdManager(session=session, client=client)
        self.announcement: AdminAnnouncementManager = AdminAnnouncementManager(
            session=session, client=client
        )
        self.role: AdminRolesManager = AdminRolesManager(session=session, client=client)
        self.invite: AdminInviteManager = AdminInviteManager(session=session, client=client)
        self.drive: AdminDriveManager = AdminDriveManager(session=session, client=client)
        self.account: AdminAccountManager = AdminAccountManager(session=session, client=client)

    @property
    def action(self) -> AdminActions:
        return AdminActions(session=self.__session, client=self.__client)

    def create_roles_model_manager(self, role_id: str | None = None) -> AdminRolesModelManager:
        return AdminRolesModelManager(
            role_id=role_id, session=self.__session, client=self.__client
        )

    def _create_client_ad_manager(self, ad_id: str) -> ClientAdminAdManager:
        return ClientAdminAdManager(ad_id=ad_id, session=self.__session, client=self.__client)

    def _create_client_announcement_manager(
        self, announce_id: str
    ) -> ClientAdminAnnouncementManager:
        return ClientAdminAnnouncementManager(
            announce_id=announce_id,
            session=self.__session,
            client=self.__client,
        )
