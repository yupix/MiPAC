from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.emoji import PartialCustomEmoji
from mipac.types.emoji import ICustomEmoji, IEmojiDetailed, IEmojiSimple

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


class EmojiSimple:
    def __init__(self, raw_emoji_simple: IEmojiSimple, *, client: ClientManager):
        self.__raw_emoji_simple: IEmojiSimple = raw_emoji_simple
        self.__client: ClientManager = client

    @property
    def aliaces(self) -> list[str]:
        return self.__raw_emoji_simple["aliaces"]

    @property
    def name(self) -> str:
        return self.__raw_emoji_simple["name"]

    @property
    def category(self) -> str | None:
        return self.__raw_emoji_simple["category"]

    @property
    def url(self) -> str:
        return self.__raw_emoji_simple["url"]

    @property
    def local_only(self) -> bool:
        return self.__raw_emoji_simple["local_only"]

    @property
    def is_sensitive(self) -> bool:
        return self.__raw_emoji_simple.get("is_sensitive", False)

    @property
    def role_ids_that_can_be_used_this_emoji_as_reaction(self) -> list[str]:
        return self.__raw_emoji_simple.get("role_ids_that_can_be_used_this_emoji_as_reaction", [])

    def _get(self, key: str) -> Any | None:
        return self.__raw_emoji_simple.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, EmojiSimple) and self.name == __value.name

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class EmojiDetailed:
    def __init__(self, raw_emoji_detailed: IEmojiDetailed, *, client: ClientManager):
        self.__raw_emoji_detailed: IEmojiDetailed = raw_emoji_detailed
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_emoji_detailed["id"]

    @property
    def aliaces(self) -> list[str]:
        return self.__raw_emoji_detailed["aliaces"]

    @property
    def name(self) -> str:
        return self.__raw_emoji_detailed["name"]

    @property
    def category(self) -> str | None:
        return self.__raw_emoji_detailed["category"]

    @property
    def host(self) -> str | None:
        return self.__raw_emoji_detailed["host"]

    @property
    def url(self) -> str:
        return self.__raw_emoji_detailed["url"]

    @property
    def is_sensitive(self) -> bool:
        return self.__raw_emoji_detailed["is_sensitive"]

    @property
    def local_only(self) -> bool:
        return self.__raw_emoji_detailed["local_only"]

    @property
    def role_ids_that_can_be_used_this_emoji_as_reaction(self) -> list[str]:
        return self.__raw_emoji_detailed["role_ids_that_can_be_used_this_emoji_as_reaction"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_emoji_detailed.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, EmojiDetailed) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
