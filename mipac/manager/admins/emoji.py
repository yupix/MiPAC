from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.emoji import AdminEmojiActions, ClientAdminEmojiActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager

class ClientAdminEmojiManager(AbstractManager):
    def __init__(self, *, emoji_id: str, session: HTTPClient, client: ClientManager):
        self.__action: ClientAdminEmojiActions = ClientAdminEmojiActions(emoji_id=emoji_id, session=session, client=client)
    
    @property
    def action(self) -> ClientAdminEmojiActions:
        return self.__action

class AdminEmojiManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__action:AdminEmojiActions = AdminEmojiActions(session=session, client=client)

    @property
    def action(self) -> AdminEmojiActions:
        return self.__action
