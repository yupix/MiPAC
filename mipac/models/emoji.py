from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.models.lite.emoji import PartialCustomEmoji

from mipac.types.emoji import ICustomEmoji

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ('CustomEmoji',)


class CustomEmoji(PartialCustomEmoji):
    """
    Attributes
    ----------
    id : str | None
        絵文字のID
    aliases : Optional[list[str]]
        絵文字のエイリアス
    category : str | None
        絵文字のカテゴリ
    host : str | None
        絵文字のホスト
    """

    def __init__(self, emoji: ICustomEmoji, *, client: ClientManager):
        super().__init__(emoji, client=client)
        self.__emoji: ICustomEmoji = emoji

    @property
    def id(self) -> str:
        return self.__emoji['id']

    @property
    def aliases(self) -> list[str]:
        return self.__emoji['aliases']

    @property
    def category(self) -> str:
        return self.__emoji['category']
