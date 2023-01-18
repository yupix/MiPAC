from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.reaction import ReactionActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ReactionManager(AbstractManager):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ReactionActions:
        """リアクションに関するアクション

        Returns
        -------
        ReactionActions
            Reactionに対するアクションを行うクラス
        """
        return ReactionActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )
