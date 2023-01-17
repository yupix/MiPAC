from typing import Optional, TypedDict

__all__ = ('EmojiPayload', 'ICustomEmojiLite', 'ICustomEmoji')


class ICustomEmojiLiteRequired(TypedDict):
    name: str


class ICustomEmojiLite(ICustomEmojiLiteRequired, total=False):
    url: str


class ICustomEmoji(ICustomEmojiLite):
    id: str
    category: str
    aliases: list[str]


class EmojiPayload(TypedDict):
    id: str | None
    aliases: Optional[list[str]]
    name: str | None
    category: str | None
    host: str | None
    url: str | None
