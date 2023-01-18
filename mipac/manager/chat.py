from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.actions.chat import BaseChatAction, ChatAction
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ('ChatManager',)


class ChatManager:
    def __init__(
        self, session: HTTPClient, client: ClientManager,
    ):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> ChatAction:
        return ChatAction(session=self.__session, client=self.__client)

    def custom_base_chat_action(
        self, user_id: str | None = None, message_id: str | None = None
    ) -> BaseChatAction:
        return BaseChatAction(
            session=self.__session,
            client=self.__client,
            user_id=user_id,
            message_id=message_id,
        )

    def custom_action(
        self, user_id: str | None = None, message_id: str | None = None
    ) -> ChatAction:
        return ChatAction(
            session=self.__session,
            client=self.__client,
            user_id=user_id,
            message_id=message_id,
        )
