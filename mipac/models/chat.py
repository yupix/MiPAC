from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.drive import File
from mipac.models.lite.user import LiteUser

if TYPE_CHECKING:
    from mipac.actions.chat import BaseChatAction
    from mipac.manager.client import ClientManager
    from mipac.types.chat import IChatGroup, IChatMessage

__all__ = ['ChatGroup', 'ChatMessage']


class ChatGroup:
    def __init__(self, group: IChatGroup, *, client: ClientManager):
        self.__group: IChatGroup = group
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """グループのID"""
        return self.__group['id']

    @property
    def created_at(self) -> str:
        """グループの作成日時"""
        return self.__group['created_at']

    @property
    def name(self) -> str:
        """グループ名"""
        return self.__group['name']

    @property
    def owner_id(self) -> str:
        """グループのオーナーのID"""
        return self.__group['owner_id']

    @property
    def user_ids(self) -> list[str]:
        return self.__group['user_ids']


class ChatMessage:
    """
    チャットオブジェクト
    """

    def __init__(self, chat: IChatMessage, *, client: ClientManager):
        self.__chat: IChatMessage = chat
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """The message ID."""
        return self.__chat['id']

    @property
    def created_at(self) -> str:
        """Returns the date and time the message was created (UTC)"""
        return self.__chat['created_at']

    @property
    def file(self) -> File | None:
        return (
            File(self.__chat['file'], client=self.__client)
            if self.__chat['file']
            else None
        )

    @property
    def text(self) -> str | None:
        """text of the message"""
        return self.__chat['text']

    @property
    def user_id(self) -> str:
        return self.__chat['user_id']

    @property
    def user(self) -> LiteUser:
        return LiteUser(self.__chat['user'], client=self.__client)

    @property
    def recipient_id(self) -> str | None:
        """ The id of the bot self """
        return self.__chat['recipient_id']

    @property
    def recipient(self) -> LiteUser | None:
        """ The user of the bot self """
        return (
            LiteUser(self.__chat['recipient'], client=self.__client)
            if self.__chat.get('recipient')
            else None
        )

    @property
    def group_id(self) -> str | None:
        return self.__chat['group_id']

    @property
    def file_id(self) -> str | None:
        return self.__chat['file_id']

    @property
    def is_read(self) -> bool:
        return bool(self.__chat['is_read'])

    @property
    def reads(self) -> list[str]:
        return self.__chat['reads']

    @property
    def group(self) -> ChatGroup | None:
        return (
            ChatGroup(self.__chat['group'], client=self.__client)
            if self.__chat.get('group')
            else None
        )

    @property
    def api(self) -> BaseChatAction:
        return self.__client.chat.custom_base_chat_action(
            user_id=self.user.id, message_id=self.id
        )
