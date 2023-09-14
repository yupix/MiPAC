from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.lite.emoji import PartialCustomEmoji
from mipac.types.emoji import ICustomEmoji

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ("CustomEmoji",)


class CustomEmoji(PartialCustomEmoji):
    def __init__(self, emoji: ICustomEmoji, *, client: ClientManager):
        super().__init__(emoji, client=client)
        self.__emoji: ICustomEmoji = emoji

    @property
    def id(self) -> str:
        return self.__emoji["id"]

    @property
    def aliases(self) -> list[str]:
        return self.__emoji["aliases"]

    @property
    def category(self) -> str:
        return self.__emoji["category"]

    @property
    def license(self) -> str | None:
        return self.__emoji["license"]

    @property
    def host(self) -> str | None:
        return self.__emoji["host"]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, CustomEmoji) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
