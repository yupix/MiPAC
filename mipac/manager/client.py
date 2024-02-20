from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.actions.client import ClientActions
from mipac.http import HTTPClient
from mipac.manager.admins.admin import AdminManager
from mipac.manager.antenna import AntennaManager
from mipac.manager.channel import ChannelManager, ClientChannelManager
from mipac.manager.chart import ChartManager
from mipac.manager.clip import ClientClipManager, ClipManager
from mipac.manager.drive.drive import DriveManager
from mipac.manager.emoji import EmojiManager
from mipac.manager.follow import FollowManager, FollowRequestManager
from mipac.manager.invite import ClientInviteManager, InviteManager
from mipac.manager.my import MyManager
from mipac.manager.note import ClientNoteManager, NoteManager
from mipac.manager.role import RoleManager
from mipac.manager.user import ClientUserManager, UserManager
from mipac.manager.username import UsernameManager

if TYPE_CHECKING:
    from mipac.config import Config
    from mipac.models.lite.user import PartialUser
    from mipac.models.user import MeDetailed


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
        return UserManager(session=self.__session, client=self)

    def _create_client_channel_manager(self, channel_id: str) -> ClientChannelManager:
        return ClientChannelManager(channel_id=channel_id, session=self.__session, client=self)

    def _create_client_note_manager(self, note_id: str) -> ClientNoteManager:
        """Create a client note manager.

        Returns
        -------
        ClientNoteManager
            The client note manager.
        """
        return ClientNoteManager(note_id=note_id, session=self.__session, client=self)

    def _create_client_invite_manager(self, invite_id: str) -> ClientInviteManager:
        return ClientInviteManager(invite_id=invite_id, session=self.__session, client=self)

    def _create_client_user_manager(self, user: PartialUser) -> ClientUserManager:
        return ClientUserManager(user=user, session=self.__session, client=self)

    def _get_client_clip_instance(self, *, clip_id: str) -> ClientClipManager:
        return ClientClipManager(clip_id=clip_id, session=self.__session, client=self)

    async def get_me(self) -> MeDetailed:
        return await self.user.action.get_me()
