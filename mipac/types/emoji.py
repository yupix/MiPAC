from typing import Optional, TypedDict

__all__ = ('EmojiPayload', 'ICustomEmojiLite')


class ICustomEmojiLite(TypedDict):
    name: str
    url: str

class EmojiPayload(TypedDict):
    id: Optional[str]
    aliases: Optional[list[str]]
    name: Optional[str]
    category: Optional[str]
    host: Optional[str]
    url: Optional[str]
