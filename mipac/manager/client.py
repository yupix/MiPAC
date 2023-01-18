from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.actions.client import ClientActions

from mipac.http import HTTPClient
from mipac.manager.admins.admin import AdminManager
from mipac.manager.chart import ChartManager
from mipac.manager.chat import ChatManager
from mipac.manager.drive import DriveManager
from mipac.manager.follow import FollowManager, FollowRequestManager
from mipac.manager.my import MyManager
from mipac.manager.note import NoteManager
from mipac.manager.user import UserManager

if TYPE_CHECKING:
    from mipac.config import Config
    from mipac.models.lite.user import LiteUser
    from mipac.models.user import UserDetailed


__all__ = ('ClientManager',)


class ClientManager:
    def __init__(self, session: HTTPClient, config: Config):
        self.__session: HTTPClient = session
        self.i = MyManager(session=session, client=self)
        self.note: NoteManager = NoteManager(session=session, client=self)
        self.chat: ChatManager = ChatManager(session=session, client=self)
        self.user: UserManager = UserManager(session=session, client=self)
        self.admin: AdminManager = AdminManager(session=session, client=self)
        self.drive: DriveManager = DriveManager(session=session, client=self)
        self.chart: ChartManager = ChartManager(session=session, client=self)
        self.follow: FollowManager = FollowManager(
            session=session, client=self,
        )
        self.follow_request: FollowRequestManager = FollowRequestManager(
            session=session, client=self,
        )
        self._config: Config = config

    @property
    def action(self) -> ClientActions:
        return ClientActions(session=self.__session, client=self)

    def _create_user_instance(self, user: LiteUser) -> UserManager:
        return UserManager(session=self.__session, client=self, user=user)

    def _create_note_instance(self, note_id: str) -> NoteManager:
        return NoteManager(note_id, session=self.__session, client=self)

    async def get_me(self) -> UserDetailed:
        return await self.user.action.get_me()
