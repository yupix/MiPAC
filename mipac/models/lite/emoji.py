from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.types.emoji import ICustomEmojiLite
from mipac.config import config

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class PartialCustomEmoji:
    def __init__(
        self, emoji: ICustomEmojiLite, *, client: ClientManager
    ) -> None:
        self.__emoji = emoji
        self.__client: ClientManager = client

    @property
    def name(self) -> str:
        return self.__emoji['name']

    @property
    def url(self) -> str | None:
        if config.use_version == 13:
            protocol = 'https' if config.is_ssl else 'http'
            url = f'{protocol}://{config.host}/emoji/{self.name}.webp'
            return url
        return self.__emoji.get('url')
