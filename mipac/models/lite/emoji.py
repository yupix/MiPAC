from __future__ import annotations

from mipac.types.emoji import ICustomEmojiLite


class PartialCustomEmoji:
    def __init__(self, emoji: ICustomEmojiLite) -> None:
        self.__emoji = emoji

    @property
    def name(self) -> str:
        return self.__emoji['name']

    @property
    def url(self) -> str:
        return self.__emoji['url']
