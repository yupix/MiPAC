from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.abc.manager import AbstractManager
from mipac.actions.user import UserActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.models.lite.user import LiteUser


__all__ = ('UserManager',)


class UserManager(AbstractManager):
    def __init__(
        self,
        user: Optional[LiteUser] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.user: Optional[LiteUser] = user

    @property
    def action(self) -> UserActions:
        return UserActions(
            session=self.__session, client=self.__client, user=self.user
        )
