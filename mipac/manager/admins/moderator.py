from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.moderator import AdminModeratorActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ('AdminModeratorManager',)


class AdminModeratorManager(AbstractManager):
    def __init__(
        self,
        user_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__user_id: str | None = user_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> AdminModeratorActions:
        """Moderatorに関するアクション

        Returns
        -------
        AdminModeratorActions
            Moderatorに対するアクションを行うクラス
        """

        return AdminModeratorActions(
            session=self.__session, client=self.__client
        )
