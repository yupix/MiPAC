from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.user import UserActions
from mipac.http import HTTPClient
from mipac.manager.follow import FollowManager

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.models.lite.user import LiteUser


__all__ = ('UserManager',)


class UserManager(AbstractManager):
    def __init__(
        self,
        user: LiteUser | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.user: LiteUser | None = user
        self.follow: FollowManager = FollowManager(
            user_id=user.id if user else None, session=session, client=client
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
