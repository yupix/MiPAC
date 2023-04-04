from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion, NotSupportVersionText
from mipac.http import HTTPClient, Route
from mipac.models.emoji import CustomEmoji
from mipac.types.emoji import ICustomEmoji

if TYPE_CHECKING:
    from mipac.client import ClientManager


class EmojiActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get(self, name: str) -> CustomEmoji:
        if self.__client._config.use_version < 13:
            raise NotSupportVersion(NotSupportVersionText)
        emoji: ICustomEmoji = await self.__session.request(
            Route('POST', '/api/emoji'), auth=True, lower=True, json={'name': name}
        )
        return CustomEmoji(emoji=emoji, client=self.__client)
