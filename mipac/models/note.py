from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Self

from mipac.abstract.model import AbstractModel
from mipac.models.lite.note import PartialNote
from mipac.models.lite.user import PartialUser
from mipac.models.poll import Poll
from mipac.types.note import (
    INote,
    INoteReaction,
    INoteState,
    INoteTranslateResult,
    INoteUpdated,
    INoteUpdatedDelete,
)
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.types.emoji import ICustomEmojiLite

__all__ = (
    "NoteState",
    "Note",
    "Header",
    "NoteReaction",
    "NoteDeleted",
    "NoteTranslateResult",
)


class NoteState(AbstractModel):
    def __init__(self, data: INoteState) -> None:
        self.__data: INoteState = data

    @property
    def is_favorite(self) -> bool:
        return self.__data["is_favorited"]

    @property
    def is_watching(self) -> bool:
        return self.__data["is_watching"]

    @property
    def is_muted_thread(self) -> bool:
        return self.__data.get("is_muted_thread", False)


class NoteDeleted(AbstractModel):
    def __init__(self, data: INoteUpdated[INoteUpdatedDelete]) -> None:
        self.__data = data

    @property
    def note_id(self) -> str:
        return self.__data["body"]["id"]

    @property
    def deleted_at(self) -> datetime:
        return str_to_datetime(self.__data["body"]["body"]["deleted_at"])

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoteDeleted) and self.note_id == __value.note_id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class Header:
    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")


class NoteReaction(AbstractModel):
    __slots__ = ("__reaction", "__client")

    def __init__(self, reaction: INoteReaction, *, client: ClientManager):
        self.__reaction: INoteReaction = reaction
        self.__client: ClientManager = client

    @property
    def id(self) -> str | None:
        return self.__reaction["id"]

    @property
    def created_at(self) -> datetime | None:
        return (
            datetime.strptime(self.__reaction["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if "created_at" in self.__reaction
            else None
        )

    @property
    def type(self) -> str | None:
        return self.__reaction["type"]

    @property
    def user(self) -> PartialUser:
        return PartialUser(self.__reaction["user"], client=self.__client)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoteReaction) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class Note(PartialNote[INote]):
    """
    Noteモデル

    Parameters
    ----------
    note: INote
        The raw data of the note

    client: ClientManager
    """

    def __init__(self, note: INote, client: ClientManager):
        super().__init__(note_data=note, client=client)

    @property
    def emojis(self) -> list[ICustomEmojiLite]:  # TODO: モデルに
        """
        Note text contains a list of emojis
        Note: emojis have been abolished since misskey v13

        Returns
        -------
        list[ICustomEmojiLite]
            List of emojis contained in note text
        """

        return self._note.get("emojis", [])

    @property
    def renote(self) -> Self | None:
        return (
            Note(note=self._note["renote"], client=self._client)
            if "renote" in self._note
            else None
        )

    @property
    def reply(self) -> Self | None:
        return (
            Note(note=self._note["reply"], client=self._client) if "reply" in self._note else None
        )

    @property
    def visible_user_ids(self) -> list[str]:
        return self._note["visible_user_ids"] if "visible_user_ids" in self._note else []

    @property
    def local_only(self) -> bool:
        return self._note["local_only"] if "local_only" in self._note else False

    @property
    def my_reaction(self) -> str | None:
        return self._note["my_reaction"] if "my_reaction" in self._note else None

    @property
    def uri(self) -> str | None:
        return self._note["uri"] if "uri" in self._note else None

    @property
    def url(self) -> str | None:
        return self._note["url"] if "url" in self._note else None

    @property
    def is_hidden(self) -> bool:
        return self._note["is_hidden"] if "is_hidden" in self._note else False

    @property
    def poll(self) -> Poll | None:
        return Poll(self._note["poll"], client=self._client) if "poll" in self._note else None


class NoteTranslateResult(AbstractModel):
    """
    NoteTranslateResult

    Parameters
    ----------
    translate_result: INoteTranslateResult
        The raw data of the note translate result
    """

    def __init__(self, translate_result: INoteTranslateResult):
        self.__translate_result = translate_result

    @property
    def source_language(self) -> str:
        return self.__translate_result["sourceLang"]

    @property
    def text(self) -> str:
        return self.__translate_result["text"]
