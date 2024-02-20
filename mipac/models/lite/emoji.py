from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.config import config
from mipac.types.emoji import ICustomEmojiLite

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class PartialCustomEmoji:
    def __init__(self, emoji: ICustomEmojiLite, *, client: ClientManager) -> None:
        self.__emoji = emoji
        self.__client: ClientManager = client

    @property
    def name(self) -> str:
        return self.__emoji["name"]

    @property
    def url(self) -> str | None:
        protocol = "https" if config.is_ssl else "http"
        url = f"{protocol}://{config.host}/emoji/{self.name}.webp"
        return url

    def _get(self, key: str) -> Any | None:
        return self.__emoji.get(key)
