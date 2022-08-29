from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.drive import File
from mipac.models.lite.user import UserLite

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.types.chat import IChatGroup, IChatMessage

__all__ = ['ChatGroup', 'ChatMessage']


class ChatGroup:
    def __init__(self, group: IChatGroup, *, client: ClientActions):
        self.__group: IChatGroup = group
        self.__client: ClientActions = client

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

    def __init__(self, chat: IChatMessage, *, client: ClientActions):
        self.__chat: IChatMessage = chat
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__chat['id']

    @property
    def created_at(self) -> str:
        return self.__chat['created_at']

    @property
    def file(self) -> File:
        return File(self.__chat['file'], client=self.__client)

    @property
    def text(self) -> str | None:
        return self.__chat['text']

    @property
    def user_id(self) -> str:
        return self.__chat['user_id']

    @property
    def user(self) -> UserLite:
        return UserLite(self.__chat['user'])

    @property
    def recipient_id(self) -> str:
        return self.__chat['recipient_id']

    @property
    def recipient(self) -> str:
        return self.__chat['recipient']

    @property
    def group_id(self) -> str:
        return self.__chat['group_id']

    @property
    def file_id(self) -> str:
        return self.__chat['file_id']

    @property
    def is_read(self) -> bool:
        return bool(self.__chat['is_read'])

    @property
    def reads(self) -> list[str]:
        return self.__chat['reads']

    @property
    def group(self) -> ChatGroup:
        return ChatGroup(self.__chat['group'], client=self.__client)
