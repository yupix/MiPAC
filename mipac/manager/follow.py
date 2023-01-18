from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.follow import FollowActions, FollowRequestActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ('FollowManager', 'FollowRequestManager')


class FollowManager(AbstractManager):
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
        self.request: FollowRequestManager = FollowRequestManager(
            user_id=user_id, session=session, client=client
        )

    @property
    def action(self) -> FollowActions:
        return FollowActions(
            user_id=self.__user_id,
            session=self.__session,
            client=self.__client,
        )


class FollowRequestManager(AbstractManager):
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
    def action(self) -> FollowRequestActions:
        return FollowRequestActions(
            user_id=self.__user_id,
            session=self.__session,
            client=self.__client,
        )
