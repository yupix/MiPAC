from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.emoji import PartialCustomEmoji
from mipac.types.note import INoteUpdated, INoteUpdatedReaction

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class PartialReaction:
    def __init__(
        self, reaction: INoteUpdated[INoteUpdatedReaction], *, client: ClientManager
    ) -> None:
        self.__reaction: INoteUpdated[INoteUpdatedReaction] = reaction
        self.__client: ClientManager = client

    @property
    def reaction(self) -> str:
        return self.__reaction["body"]["body"]["reaction"]

    @property
    def emoji(self) -> PartialCustomEmoji:
        return PartialCustomEmoji(self.__reaction["body"]["body"]["emoji"], client=self.__client)

    @property
    def user_id(self) -> str:
        return self.__reaction["body"]["body"]["user_id"]

    def _get(self, key: str) -> Any | None:
        return self.__reaction.get(key)
