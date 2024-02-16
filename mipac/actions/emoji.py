from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.emoji import EmojiDetailed, EmojiSimple
from mipac.types.emoji import IEmojiDetailed, IEmojiSimple

if TYPE_CHECKING:
    from mipac.client import ClientManager


class EmojiActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get(self, name: str) -> EmojiDetailed:
        emoji: IEmojiDetailed = await self.__session.request(
            Route("POST", "/api/emoji"), auth=True, lower=True, json={"name": name}
        )
        return EmojiDetailed(raw_emoji_detailed=emoji, client=self.__client)

    async def gets(self, name: str) -> EmojiSimple:
        emoji: IEmojiSimple = await self.__session.request(
            Route("POST", "/api/emojis"), auth=True, lower=True, json={"name": name}
        )
        return EmojiSimple(raw_emoji_simple=emoji, client=self.__client)
