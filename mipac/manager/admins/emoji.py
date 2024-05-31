from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.admins.emoji import AdminEmojiAction, ClientAdminEmojiAction
from mipac.http import HTTPClient
from mipac.manager.client import ClientManager

if TYPE_CHECKING:
    from mipac.client import ClientManager

class ClientAdminEmojiManager(AbstractManager):
    def __init__(self, *, emoji_id: str, session: HTTPClient, client: ClientManager):
        self.__action: ClientAdminEmojiAction = ClientAdminEmojiAction(emoji_id=emoji_id, session=session, client=client)
    
    @property
    def action(self) -> ClientAdminEmojiAction:
        return self.__action

class AdminEmojiManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__action:AdminEmojiAction = AdminEmojiAction(session=session, client=client)

    @property
    def action(self) -> AdminEmojiAction:
        return self.__action
