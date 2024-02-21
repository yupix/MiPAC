from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.follow import ClientFollowActions, FollowActions, FollowRequestActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ("FollowManager", "FollowRequestManager")


class ClientFollowManager(AbstractManager):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        # self.request: ClientFollowRequestManager = ClientFollowRequestManager(
        #     session=session, client=client
        # )
        self.__action: ClientFollowActions = ClientFollowActions(
            user_id=user_id,
            session=session,
            client=client,
        )

    @property
    def action(self) -> ClientFollowActions:
        return self.__action


class FollowManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.request: FollowRequestManager = FollowRequestManager(session=session, client=client)
        self.__action: FollowActions = FollowActions(
            session=self.__session,
            client=self.__client,
        )

    @property
    def action(self) -> FollowActions:
        return self.__action


class FollowRequestManager(AbstractManager):
    def __init__(self, user_id: str | None = None, *, session: HTTPClient, client: ClientManager):
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
