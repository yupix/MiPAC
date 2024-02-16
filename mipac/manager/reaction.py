from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.reaction import ClientReactionActions, ReactionActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientReactionManager(AbstractManager):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action = ClientReactionActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )

    @property
    def action(self) -> ClientReactionActions:
        """リアクションに関するアクション

        Returns
        -------
        ClientReactionActions
            Reactionに対するアクションを行うクラス
        """
        return self.__action


class ReactionManager(AbstractManager):
    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.__action = ReactionActions(
            session=self.__session,
            client=self.__client,
        )

    @property
    def action(self) -> ReactionActions:
        """リアクションに関するアクション

        Returns
        -------
        ReactionActions
            Reactionに対するアクションを行うクラス
        """
        return self.__action
