from __future__ import annotations

from mipac.models.lite.emoji import PartialCustomEmoji
from mipac.types.note import INoteUpdated, INoteUpdatedReaction


class PartialReaction:
    def __init__(self, reaction: INoteUpdated[INoteUpdatedReaction]) -> None:
        self.__reaction = reaction

    @property
    def reaction(self) -> str:
        return self.__reaction['body']['body']['reaction']

    @property
    def emoji(self) -> PartialCustomEmoji:
        return PartialCustomEmoji(self.__reaction['body']['body']['emoji'])

    @property
    def user_id(self) -> str:
        return self.__reaction['body']['user_id']
