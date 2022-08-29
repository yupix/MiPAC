from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.types.emoji import ICustomEmoji

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('CustomEmoji',)


class CustomEmoji:
    """
    Attributes
    ----------
    id : Optional[str]
        絵文字のID
    aliases : Optional[list[str]]
        絵文字のエイリアス
    name : Optional[str]
        絵文字の名前
    category : Optional[str]
        絵文字のカテゴリ
    host : Optional[str]
        絵文字のホスト
    url : Optional[str]
        絵文字のURL
    """

    __slots__ = (
        '__emoji',
        '__client',
    )

    def __init__(self, emoji: ICustomEmoji, *, client: ClientActions):
        self.__emoji: ICustomEmoji = emoji
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__emoji['id']

    @property
    def aliases(self) -> list[str]:
        return self.__emoji['aliases']

    @property
    def name(self) -> str:
        return self.__emoji['name']

    @property
    def category(self) -> str:
        return self.__emoji['category']

    @property
    def url(self) -> str:
        return self.__emoji['url']
