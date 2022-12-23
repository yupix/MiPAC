from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.manager.client import ClientActions
from mipac.manager.reaction import ReactionManager
from mipac.models.lite.user import LiteUser
from mipac.models.note import Note

if TYPE_CHECKING:
    from mipac.types.notification import IReactionNf


class NotificationReaction:
    def __init__(
        self, reaction: IReactionNf, *, client: ClientActions
    ) -> None:
        self.__reaction: IReactionNf = reaction
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__reaction['id']

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(
            self.__reaction['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )

    @property
    def type(self) -> str:
        return self.__reaction['type']

    @property
    def is_read(self) -> bool:
        return self.__reaction['is_read']

    @property
    def user(self) -> LiteUser:
        return LiteUser(self.__reaction['user'], client=self.__client)

    @property
    def note(self) -> Note:
        return Note(self.__reaction['note'], client=self.__client)

    @property
    def reaction(self) -> str:
        return self.__reaction['reaction']

    @property
    def action(self) -> ReactionManager:
        return self.__client.reaction
