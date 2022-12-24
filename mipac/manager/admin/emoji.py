from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admin.emoji import AdminEmojiActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminEmojiManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    @property
    def action(self) -> AdminEmojiActions:
        return AdminEmojiActions(session=self.__session, client=self.__client)

    def _create_admin_emoji_instance(self, emoji_id: str) -> AdminEmojiActions:
        return AdminEmojiActions(
            emoji_id=emoji_id, session=self.__session, client=self.__client
        )
