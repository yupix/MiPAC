from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.drive import File
from mipac.models.lite.user import PartialUser
from mipac.models.poll import Poll
from mipac.types.note import (
    INote,
    INoteChannel,
    INoteReaction,
    INoteState,
    INoteTranslateResult,
    INoteUpdated,
    INoteUpdatedDelete,
    INoteVisibility,
)
from mipac.types.reaction import IReactionAcceptance
from mipac.utils.format import str_to_datetime
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.note import ClientNoteManager


__all__ = (
    "NoteState",
    "Note",
    "NoteReaction",
    "NoteDeleted",
    "NoteTranslateResult",
)


class NoteState:
    def __init__(self, data: INoteState) -> None:
        self.__data: INoteState = data

    @property
    def is_favorite(self) -> bool:
        return self.__data["is_favorited"]

    @property
    def is_muted_thread(self) -> bool:
        return self.__data["is_muted_thread"]

    def _get(self, key: str) -> Any | None:
        return self.__data.get(key)


class NoteDeleted:
    def __init__(self, data: INoteUpdated[INoteUpdatedDelete]) -> None:
        self.__data = data

    @property
    def note_id(self) -> str:
        return self.__data["body"]["id"]

    @property
    def deleted_at(self) -> datetime:
        return str_to_datetime(self.__data["body"]["body"]["deleted_at"])

    def _get(self, key: str) -> Any | None:
        return self.__data.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoteDeleted) and self.note_id == __value.note_id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class NoteReaction:
    __slots__ = ("__reaction", "__client")

    def __init__(self, raw_reaction: INoteReaction, *, client: ClientManager):
        self.__reaction: INoteReaction = raw_reaction
        self.__client: ClientManager = client

    @property
    def id(self) -> str | None:
        """note reactionId

        Returns
        -------
        str | None
            note reactionId
        """
        return self.__reaction["id"]

    @property
    def created_at(self) -> datetime | None:
        """note createdAt

        Returns
        -------
        datetime | None
            note createdAt
        """
        return (
            str_to_datetime(self.__reaction["created_at"])
            if "created_at" in self.__reaction
            else None
        )

    @property
    def user(self) -> PartialUser:
        """note user

        Returns
        -------
        PartialUser
            note user
        """
        return PartialUser(self.__reaction["user"], client=self.__client)

    @property
    def type(self) -> str | None:
        """reaction type

        Returns
        -------
        str | None
            reaction type
        """
        return self.__reaction["type"]

    def _get(self, key: str) -> Any | None:
        return self.__reaction.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoteReaction) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class NoteChannel:
    def __init__(self, raw_note_channel: INoteChannel, *, client: ClientManager) -> None:
        self.__raw_note_channel: INoteChannel = raw_note_channel
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """note channelId

        Returns
        -------
        str
            note channelId
        """
        return self.__raw_note_channel["id"]

    @property
    def name(self) -> str:
        """note channelName

        Returns
        -------
        str
            note channelName
        """
        return self.__raw_note_channel["name"]

    @property
    def color(self) -> str:
        """note channelColor

        Returns
        -------
        str
            note channelColor
        """
        return self.__raw_note_channel["color"]

    @property
    def is_sensitive(self) -> bool:
        """note channelIsSensitive

        Returns
        -------
        bool
            note channelIsSensitive
        """
        return self.__raw_note_channel["is_sensitive"]

    @property
    def allow_renote_to_external(self) -> bool:
        """note channelAllowRenoteToExternal

        Returns
        -------
        bool
            note channelAllowRenoteToExternal
        """
        return self.__raw_note_channel["allow_renote_to_external"]

    @property
    def user_id(self) -> str | None:
        """note channelUserId

        Returns
        -------
        str | None
            note channelUserId
        """
        return self.__raw_note_channel["user_id"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_note_channel.get(key)


class Note:
    """Noteモデル

    Parameters
    ----------
    note: INote
        The raw data of the note

    client: ClientManager
    """

    def __init__(self, raw_note: INote, client: ClientManager):
        self.__raw_note: INote = raw_note
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """
        note id

        Returns
        -------
        str
            note id
        """
        return self.__raw_note["id"]

    @property
    def created_at(self) -> datetime:
        """note createdAt

        Returns
        -------
        datetime
            note createdAt
        """
        return str_to_datetime(self.__raw_note["created_at"])

    @property
    def deleted_at(self) -> datetime | None:
        """note deletedAt

        Returns
        -------
        datetime | None
            note deletedAt
        """
        return (
            str_to_datetime(self.__raw_note["deleted_at"])
            if "deleted_at" in self.__raw_note
            else None
        )

    @property
    def text(self) -> str | None:
        """note text

        Returns
        -------
        str | None
            note text
        """
        return self.__raw_note.get("text")

    @property
    @deprecated
    def content(self) -> str | None:
        """note content

        .. deprecated:: 0.6.0
            Use :meth:`mipac.models.note.Note.text` instead.

        Returns
        -------
        str | None
            note content
        """
        return self.text

    @property
    def cw(self) -> str | None:
        """note cw

        Returns
        -------
        str | None
            note cw
        """
        return self.__raw_note.get("cw")

    @property
    def user_id(self) -> str:
        """note userId

        Returns
        -------
        str
            note userId
        """
        return self.__raw_note["user_id"]

    @property
    @deprecated
    def author(self) -> PartialUser:
        """note author

        .. deprecated:: 0.6.0
            Use :meth:`mipac.models.note.Note.user` instead.


        Returns
        -------
        PartialUser
            note author
        """
        return PartialUser(self.__raw_note["user"], client=self.__client)

    @property
    def user(self) -> PartialUser:
        """note author

        Returns
        -------
        PartialUser
            note user
        """
        return PartialUser(self.__raw_note["user"], client=self.__client)

    @property
    def reply_id(self) -> str | None:
        """note replyId

        Returns
        -------
        str | None
            note replyId
        """
        return self.__raw_note["reply_id"]

    @property
    def renote_id(self) -> str | None:
        """note renoteId

        Returns
        -------
        str | None
            note renoteId
        """
        return self.__raw_note["renote_id"]

    @property
    def reply(self) -> Note | None:
        """note reply

        Returns
        -------
        Note | None
            note reply
        """
        return (
            Note(self.__raw_note["reply"], client=self.__client)
            if "reply" in self.__raw_note
            else None
        )

    @property
    def renote(self) -> Note | None:
        """note renote

        Returns
        -------
        Note | None
            note renote
        """
        return (
            Note(self.__raw_note["renote"], client=self.__client)
            if "renote" in self.__raw_note
            else None
        )

    @property
    def is_hidden(self) -> bool | None:
        """note isHidden

        Returns
        -------
        bool | None
            note isHidden
        """
        return self.__raw_note.get("is_hidden")

    @property
    def visibility(self) -> INoteVisibility:
        """note visibility

        Returns
        -------
        INoteVisibility
            note visibility
        """
        return self.__raw_note["visibility"]

    @property
    def mentions(self) -> list[str]:
        """note mentions

        Returns
        -------
        list[str]
            note mentions
        """
        return self.__raw_note.get("mentions", [])

    @property
    def visible_user_ids(self) -> list[str]:
        """note visibleUserIds

        Returns
        -------
        list[str] | None
            note visibleUserIds
        """
        return self.__raw_note.get("visible_user_ids", [])

    @property
    def file_ids(self) -> list[str]:
        """note fileIds

        Returns
        -------
        list[str]
            note fileIds
        """
        return self.__raw_note["file_ids"]

    @property
    def files(self) -> list[File]:
        """note files

        Returns
        -------
        list[IFile]
            note files
        """
        return [File(raw_file, client=self.__client) for raw_file in self.__raw_note["files"]]

    @property
    def tags(self) -> list[str]:
        """note tags

        Returns
        -------
        list[str] | None
            note tags
        """
        return self.__raw_note.get("tags", [])

    @property
    def poll(self) -> Poll | None:
        """note poll

        Returns
        -------
        IPoll | None
            note poll
        """
        return (
            Poll(self.__raw_note["poll"], client=self.__client)
            if "poll" in self.__raw_note
            else None
        )

    @property
    def emojis(self) -> dict[str, str]:
        """note emojis

        Returns
        -------
        dict[str, str]
            note emojis
        """
        return self.__raw_note["emojis"]

    @property
    def channel_id(self) -> str | None:
        """note channelId

        Returns
        -------
        str | None
            note channelId
        """
        return self.__raw_note.get("channel_id")

    @property
    def channel(self) -> NoteChannel | None:
        """note channel

        Returns
        -------
        NoteChannel | None
            note channel
        """
        return (
            NoteChannel(self.__raw_note["channel"], client=self.__client)
            if "channel" in self.__raw_note and self.__raw_note["channel"]
            else None
        )

    @property
    def local_only(self) -> bool:
        """note localOnly

        Returns
        -------
        bool
            note localOnly
        """
        return self.__raw_note["local_only"]

    @property
    def reaction_acceptance(self) -> IReactionAcceptance:
        """note reactionAcceptance

        Returns
        -------
        IReactionAcceptance
            note reactionAcceptance
        """
        return self.__raw_note["reaction_acceptance"]

    @property
    def reactions(self) -> dict[str, int]:
        """note reactions

        Returns
        -------
        dict[str, int]
            note reactions
        """
        return self.__raw_note["reactions"]

    @property
    def renote_count(self) -> int:
        """note renoteCount

        Returns
        -------
        int
            note renoteCount
        """
        return self.__raw_note["renote_count"]

    @property
    def replies_count(self) -> int:
        """note repliesCount

        Returns
        -------
        int
            note repliesCount
        """
        return self.__raw_note["replies_count"]

    @property
    def uri(self) -> str | None:
        """note uri

        Returns
        -------
        str
            note uri
        """
        return self.__raw_note.get("uri")

    @property
    def url(self) -> str | None:
        """note url

        Returns
        -------
        str
            note url
        """
        return self.__raw_note.get("url")

    @property
    def reaction_and_user_pair_cache(self) -> dict[str, list[PartialUser]]:
        """note reactionAndUserPairCache

        Returns
        -------
        dict[str, list[PartialUser]]
            note reactionAndUserPairCache
        """
        if "reaction_and_user_pair_cache" not in self.__raw_note:
            return {}
        reaction_and_user_pair_cache = {}

        for k, v in self.__raw_note["reaction_and_user_pair_cache"].items():
            reaction_and_user_pair_cache[k] = [
                PartialUser(user, client=self.__client) for user in v
            ]
        return reaction_and_user_pair_cache

    @property
    def clipped_count(self) -> int | None:
        """note clippedCount

        Returns
        -------
        int | None
            note clippedCount
        """
        return self.__raw_note.get("clipped_count")

    @property
    def my_reaction(self) -> str | None:
        """note myReaction

        Returns
        -------
        str | None
            note myReaction
        """
        return self.__raw_note.get("my_reaction")

    @property
    def api(self) -> ClientNoteManager:
        """note api

        Returns
        -------
        ClientNoteManager
            note api
        """
        return self.__client._create_client_note_manager(note_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self.__raw_note.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Note) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class NoteTranslateResult:
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

    def _get(self, key: str) -> Any | None:
        return self.__translate_result.get(key)
