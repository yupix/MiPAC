from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.user import UserActions
from mipac.http import HTTPClient
from mipac.manager.follow import FollowManager
from mipac.manager.mute import MuteManager

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.models.lite.user import LiteUser


__all__ = ('UserManager',)


class UserManager(AbstractManager):
    def __init__(
        self,
        user: LiteUser | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        user_id: str | None = user.id if user else None
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.user: LiteUser | None = user
        self.follow: FollowManager = FollowManager(
            user_id=user_id, session=session, client=client
        )
        self.mute: MuteManager = MuteManager(
            user_id=user_id, session=session, client=client
        )

    @property
    def action(self) -> UserActions:
        """ユーザーに対するアクション

        Returns
        -------
        UserActions
            ユーザーに対するアクションを行うクラス
        """
        return UserActions(
            session=self.__session, client=self.__client, user=self.user
        )
