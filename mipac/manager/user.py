from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.user import ClientUserActions, UserActions
from mipac.http import HTTPClient
from mipac.manager.blocking import BlockingManager
from mipac.manager.follow import FollowManager
from mipac.manager.mute import MuteManager
from mipac.manager.users.list import ClientUserListManager, UserListManager

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.models.lite.user import PartialUser


__all__ = ("UserManager", "ClientUserManager")


class ClientUserManager(AbstractManager):
    def __init__(self, user: PartialUser, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action: ClientUserActions = ClientUserActions(
            user=user, session=session, client=client
        )
        # self.follow: FollowManager = FollowManager(session=session, client=client)  TODO: Client版のFollowManagerを作る
        # self.mute: MuteManager = MuteManager(session=session, client=client)  TODO: Client版のMuteManagerを作る
        # self.block = BlockingManager(session=session, client=client)  TODO: Client版のBlockingManagerを作る
        self.list = ClientUserListManager(user_id=user.id, session=session, client=client)

    @property
    def action(self) -> ClientUserActions:
        return self.__action


class UserManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.follow: FollowManager = FollowManager(session=session, client=client)
        self.mute: MuteManager = MuteManager(session=session, client=client)
        self.block = BlockingManager(session=session, client=client)
        self.list = UserListManager(session=session, client=client)
        self.__actions: UserActions = UserActions(session=session, client=client)

    @property
    def action(self) -> UserActions:
        return self.__actions

    def _create_client_user_list_manager(
        self, list_id: str, user_id: str | None = None
    ) -> ClientUserListManager:
        return ClientUserListManager(
            list_id=list_id, user_id=user_id, session=self.__session, client=self.__client
        )
