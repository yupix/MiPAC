from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.actions.client import ClientActions
from mipac.http import HTTPClient
from mipac.manager.admins.admin import AdminManager
from mipac.manager.antenna import AntennaManager
from mipac.manager.channel import ChannelManager
from mipac.manager.chart import ChartManager
from mipac.manager.clip import ClipManager
from mipac.manager.drive import DriveManager
from mipac.manager.emoji import EmojiManager
from mipac.manager.follow import FollowManager, FollowRequestManager
from mipac.manager.invite import ClientInviteManager, InviteManager
from mipac.manager.my import MyManager
from mipac.manager.note import ClientNoteManager, NoteManager
from mipac.manager.role import RoleManager
from mipac.manager.user import UserManager
from mipac.manager.username import UsernameManager

if TYPE_CHECKING:
    from mipac.config import Config
    from mipac.models.lite.user import PartialUser
    from mipac.models.user import UserDetailed


__all__ = ("ClientManager",)


class ClientManager:
    def __init__(self, session: HTTPClient, config: Config):
        self.__session: HTTPClient = session
        self.i = MyManager(session=session, client=self)
        self.note: NoteManager = NoteManager(session=session, client=self)
        self.user: UserManager = UserManager(session=session, client=self)
        self.admin: AdminManager = AdminManager(session=session, client=self)
        self.drive: DriveManager = DriveManager(session=session, client=self)
        self.chart: ChartManager = ChartManager(session=session, client=self)
        self.channel: ChannelManager = ChannelManager(session=session, client=self)
        self.follow: FollowManager = FollowManager(
            session=session,
            client=self,
        )
        self.follow_request: FollowRequestManager = FollowRequestManager(
            session=session,
            client=self,
        )
        self.clip: ClipManager = ClipManager(session=session, client=self)
        self.emoji: EmojiManager = EmojiManager(session=session, client=self)
        self.antenna: AntennaManager = AntennaManager(session=session, client=self)
        self.role: RoleManager = RoleManager(session=session, client=self)
        self.username: UsernameManager = UsernameManager(session=session, client=self)
        self.invite: InviteManager = InviteManager(session=session, client=self)
        self._config: Config = config

    @property
    def action(self) -> ClientActions:
        return ClientActions(session=self.__session, client=self)

    def _create_user_instance(self, user: PartialUser) -> UserManager:
        return UserManager(session=self.__session, client=self, user=user)

    def _create_note_instance(self, note_id: str) -> NoteManager:
        return NoteManager(note_id, session=self.__session, client=self)

    def _create_channel_instance(self, channel_id: str) -> ChannelManager:
        return ChannelManager(channel_id=channel_id, session=self.__session, client=self)

    def _create_client_note_manager(self, note_id: str) -> ClientNoteManager:
        return ClientNoteManager(note_id=note_id, session=self.__session, client=self)

    def _create_client_invite_manager(self, invite_id: str) -> ClientInviteManager:
        return ClientInviteManager(invite_id=invite_id, session=self.__session, client=self)

    async def get_me(self) -> UserDetailed:
        return await self.user.action.get_me()
