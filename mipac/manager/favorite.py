from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.favorite import FavoriteActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class FavoriteManager(AbstractManager):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__note_id = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> FavoriteActions:
        """お気に入りに関するアクション

        Returns
        -------
        ReactionActions
            お気に入りに対するアクションを行うクラス
        """
        return FavoriteActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )
