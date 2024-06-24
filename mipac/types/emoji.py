from typing import NotRequired, Optional, TypedDict

__all__ = ("EmojiPayload", "ICustomEmojiLite", "ICustomEmoji")


class ICustomEmojiLiteRequired(TypedDict):
    name: str


class ICustomEmojiLite(ICustomEmojiLiteRequired, total=False):
    url: str


class ICustomEmoji(ICustomEmojiLite):
    id: str
    category: str
    aliases: list[str]
    host: str | None
    license: str | None  # v13 only


class EmojiPayload(TypedDict):
    id: str | None
    aliases: Optional[list[str]]
    name: str | None
    category: str | None
    host: str | None
    url: str | None
    license: str | None  # v13 only


class IEmojiSimple(TypedDict):
    aliaces: list[str]
    name: str
    category: str | None
    url: str
    local_only: bool
    is_sensitive: NotRequired[bool]
    role_ids_that_can_be_used_this_emoji_as_reaction: NotRequired[list[str]]


class IEmojiDetailed(TypedDict):
    id: str
    aliaces: list[str]
    name: str
    category: str | None
    host: str | None
    url: str
    license: str | None
    is_sensitive: bool
    local_only: bool
    role_ids_that_can_be_used_this_emoji_as_reaction: list[str]
