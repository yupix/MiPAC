from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.errors.base import APIError
from mipac.file import MiFile
from mipac.http import HTTPClient, Route
from mipac.models.clip import Clip
from mipac.models.drive import File
from mipac.models.note import Note, NoteReaction, NoteState, NoteTranslateResult
from mipac.models.poll import MiPoll, Poll
from mipac.types.clip import IClip
from mipac.types.note import ICreatedNote, INote, INoteState, INoteTranslateResult, INoteVisibility
from mipac.types.reaction import IReactionAcceptance
from mipac.utils.cache import cache
from mipac.utils.format import remove_dict_empty, remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING, check_multi_arg, deprecated

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ["NoteActions"]


def create_note_body(
    text: str | None = None,
    visibility: INoteVisibility = MISSING,
    visible_user_ids: list[str] = MISSING,
    cw: str | None = None,
    local_only: bool = MISSING,
    reaction_acceptance: IReactionAcceptance = None,
    no_extract_mentions: bool = MISSING,
    no_extract_hashtags: bool = MISSING,
    no_extract_emojis: bool = MISSING,
    reply_id: str | None = None,
    renote_id: str | None = None,
    channel_id: str | None = None,
    files: list[MiFile | File | str] = MISSING,
    media_ids: list[str] = MISSING,
    poll: MiPoll | None = None,
):
    text = text or None
    body = {
        "visibility": visibility,
        "visibleUserIds": visible_user_ids,
        "text": text,
        "mediaIds": media_ids,
        "cw": cw,
        "localOnly": local_only,
        "reactionAcceptance": reaction_acceptance,
        "noExtractMentions": no_extract_mentions,
        "noExtractHashtags": no_extract_hashtags,
        "noExtractEmojis": no_extract_emojis,
        "replyId": reply_id,
        "renoteId": renote_id,
        "channelId": channel_id,
    }
    if not check_multi_arg(text, files, renote_id, poll):
        raise ValueError("To send a note, one of content, file_ids, renote_id or poll is required")

    if poll and type(Poll):
        poll_data = remove_dict_empty(
            {
                "choices": poll.choices,
                "multiple": poll.multiple,
                "expiresAt": poll.expires_at,
                "expiredAfter": poll.expired_after,
            }
        )
        body["poll"] = poll_data
    if isinstance(files, MISSING) is False:
        file_ids = []
        for file in files:
            if isinstance(file, MiFile):
                file_ids.append(file.file_id)
            elif isinstance(file, File):
                file_ids.append(file.id)
            elif isinstance(file, str):
                file_ids.append(file)
            else:
                raise ValueError("files must be MiFile or str or File")
        body["fileIds"] = file_ids

    return remove_dict_missing(body)


class SharedNoteActions(AbstractAction):
    def __init__(
        self,
        session: HTTPClient,
        client: ClientManager,
    ):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @cache(group="get_note_children")
    async def get_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
        *,
        note_id: str,
    ) -> list[Note]:
        return await self.fetch_children(
            limit=limit, since_id=since_id, untilId=untilId, note_id=note_id
        )

    @cache(group="get_note_children", override=True)
    async def fetch_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
        *,
        note_id: str,
    ) -> list[Note]:
        """Get children of the note.
        update the cache of the :py:meth:`mipac.actions.note.ClientNoteActions.get_children` method

        Endpoint: `/api/notes/children`

        Parameters
        ----------
        limit : int, default=100
            limit
        since_id : str | None, default=None
            Since ID
        untilId : str | None, default=None
            Until ID
        note_id : str | None, default=None
            note id

        Returns
        -------
        list[Note]
            Children of the note
        """
        data = {
            "noteId": note_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": untilId,
        }

        notes: list[INote] = await self._session.request(
            Route("POST", "/api/notes/children"), json=data
        )
        return [Note(note, self._client) for note in notes]

    async def get_all_children(
        self,
        limit: int = 10,
        since_id: str | None = None,
        untilId: str | None = None,
        *,
        note_id: str,
    ) -> AsyncGenerator[Note, None]:
        """Get all children of the note

        Endpoint: `/api/notes/children`

        Parameters
        ----------
        since_id : str | None, default=None
            Since ID
        untilId : str | None, default=None
            Until ID
        note_id : str | None, default=None
            note id

        Returns
        -------
        AsyncGenerator[Note, None]
            Children of the note
        """
        data = {
            "noteId": note_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": untilId,
        }

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/notes/children"), json=data
        )

        while pagination.is_final is False:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, self._client)

    async def get_clips(self, *, note_id: str) -> list[Clip]:
        """Get the clips of the note

        Endpoint: `/api/notes/clips`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        list[Clip]
            Clips of the note
        """
        data = {"noteId": note_id}
        res: list[IClip] = await self._session.request(
            Route("POST", "/api/notes/clips"), json=data, auth=True
        )
        return [Clip(clip, client=self._client) for clip in res]

    async def get_conversation(
        self, limit: int = 10, offset: int = 0, *, note_id: str
    ) -> list[Note]:
        """Get the conversation of the note

        Endpoint: `/api/notes/conversation`

        Parameters
        ----------
        limit : int, default=10
            limit
        offset : int, default=0
            offset
        note_id : str | None, default=None
            note id

        Returns
        -------
        list[Note]
            Notes of the conversation
        """
        data = {"noteId": note_id, "limit": limit, "offset": offset}
        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/conversation"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    async def delete(self, *, note_id: str) -> bool:
        """Delete a note

        Endpoint: `/api/notes/delete`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        bool
            success or not
        """
        data = {"noteId": note_id}
        res = await self._session.request(Route("POST", "/api/notes/delete"), json=data, auth=True)
        return bool(res)

    async def get_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str,
    ) -> list[NoteReaction]:
        return await self._client.note.reaction.action.get_reactions(
            type=type, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )

    async def fetch_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str,
    ) -> list[NoteReaction]:
        return await self._client.note.reaction.action.fetch_reactions(
            note_id=note_id, type=type, limit=limit, since_id=since_id, until_id=until_id
        )

    async def get_renotes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str,
    ) -> list[Note]:
        """Get renote of the note

        Endpoint: `/api/notes/renotes`

        Parameters
        ----------
        limit : int, default=10
            limit
        since_id : str | None, default=None
            Since ID
        until_id : str | None, default=None
            Until ID
        note_id : str | None, default=None
            note id

        Returns
        -------
        list[Note]
            Renotes of the note
        """
        data = {
            "noteId": note_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/renotes"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    async def get_replies(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        note_id: str,
    ) -> list[Note]:
        """Get replies to the specified note

        Endpoint: `/api/notes/replies`

        Parameters
        ----------
        since_id : str | None, default=None
            ID to get replies since this ID (exclusive)
        until_id : str | None, default=None
            ID to get replies until this ID (exclusive)
        limit : int, default=10
            Maximum number of replies to retrieve
        note_id : str
            ID of the note to get replies for

        Returns
        -------
        list[Note]
            List of reply notes
        """
        data = {
            "noteId": note_id,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
        }
        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/replies"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    async def get_all_replies(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        note_id: str,
    ) -> AsyncGenerator[Note, None]:
        """Get replies to the note

        Endpoint: `/api/notes/replies`

        Parameters
        ----------
        since_id : str | None, default=None
            since id
        until_id : str | None, default=None
            until id
        note_id: str | None, default=None
            note id

        Returns
        -------
        AsyncGenerator[Note, None]
            replies
        """
        body = {"noteId": note_id, "sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/notes/replies"), json=body
        )

        while pagination.is_final is False:
            res_notes = await pagination.next()
            for res_note in res_notes:
                yield Note(res_note, client=self._client)

    @cache(group="get_note_state")
    async def get_state(self, *, note_id: str) -> NoteState:
        """Get the state of the note

        Endpoint: `/api/notes/state`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        NoteState
            Note state
        """
        return await self.fetch_state(note_id=note_id)

    @cache(group="get_note_state", override=True)
    async def fetch_state(self, *, note_id: str) -> NoteState:
        """Get the state of the note.

        update the cache of the :py:meth:`mipac.actions.note.ClientNoteActions.get_state` method

        Endpoint: `/api/notes/state`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        NoteState
            Note state
        """
        data = {"noteId": note_id}
        res: INoteState = await self._session.request(
            Route("POST", "/api/notes/state"), auth=True, json=data
        )
        return NoteState(res)

    async def add_clips(self, clip_id: str, *, note_id: str) -> bool:
        """Add a note to the clip

        Endpoint: `/api/clips/add-note`

        Parameters
        ----------
        note_id : str | None, default=None
            note id
        clip_id : str
            clip id

        Returns
        -------
        bool
            success or not
        """
        data = {"noteId": note_id, "clipId": clip_id}
        return bool(
            await self._session.request(Route("POST", "/api/clips/add-note"), json=data, auth=True)
        )

    async def create_renote(self, *, note_id: str) -> Note:
        """Renote a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        Note
            Renoted note
        """
        body = create_note_body(renote_id=note_id)
        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            auth=True,
            lower=True,
        )
        return Note(res["created_note"], client=self._client)

    async def renote(
        self,
        text: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        channel_id: str | None = None,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
        *,
        renote_id: str,
    ):
        """Renote a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str | None, default=None
            text
        visibility : INoteVisibility, default='public'
            Disclosure range
        visible_user_ids : list[str] | None, default=None
            List of users to be published
        cw : str | None, default=None
            Text to be displayed when warning is given
        local_only : bool, default=False
            Whether to show only locally or not
        reaction_acceptance : IReactionAcceptance, default=None
            Reaction acceptance setting
        no_extract_mentions : bool, default=TrueMISSING
            Whether to expand the mention
        no_extract_hashtags : bool, default=MISSING
            Whether to expand the hashtag
        no_extract_emojis : bool, default=MISSING
            Whether to expand the emojis
        channel_id : str | None, default=None
            Channel ID
        files : list[MiFile | File | str] | None, default=None
            The ID list of files to be attached
        poll : MiPoll | None, default=None
        """
        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            renote_id=renote_id,
            channel_id=channel_id,
            files=files,
            poll=poll,
        )

        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            auth=True,
            lower=True,
        )

        return Note(res["created_note"], client=self._client)

    async def reply(
        self,
        text: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
        *,
        reply_id: str,
    ) -> Note:
        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            reply_id=reply_id,
            files=files,
            poll=poll,
        )
        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            lower=True,
            auth=True,
        )
        return Note(res["created_note"], client=self._client)

    async def create_quote(
        self,
        content: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
        *,
        note_id: str,
    ) -> Note:
        """Create a note quote.

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        content: str | None, default=None
            text
        visibility: INoteVisibility, default='public'
            Disclosure range
        visible_user_ids: list[str] | None, default=None
            List of users to be published
        cw: str | None, default=None
            Text to be displayed when warning is given
        local_only: bool, default=False
            Whether to show only locally or not
        extract_mentions: bool, default=True
            Whether to expand the mention
        extract_hashtags: bool, default=True
            Whether to expand the hashtag
        extract_emojis: bool, default=True
            Whether to expand the emojis
        files: list[MiFile | File | str] | None, default=None
            The ID list of files to be attached
        poll: MiPoll | None, default=None
            Questionnaire to be created
        note_id: str | None, default=None
            Note IDs to target for renote and citations
        """
        body = create_note_body(
            text=content,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            renote_id=note_id,
            files=files,
            poll=poll,
        )
        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            auth=True,
            lower=True,
        )

        return Note(res["created_note"], client=self._client)

    @cache(group="translate_note")
    async def translate(
        self,
        target_lang: str = "en-US",
        *,
        note_id: str,
    ) -> NoteTranslateResult:
        """Translate a note

        Endpoint: `/api/notes/translate`

        Parameters
        ----------
        note_id : str | None, default=None
            Note ID to target for translation
        target_lang : str, default='en'
            Target language

        Returns
        -------
        NoteTranslateResult
            Translated result
        """
        data = {"noteId": note_id, "targetLang": target_lang}
        res: INoteTranslateResult = await self._session.request(
            Route("POST", "/api/notes/translate"), json=data, auth=True
        )
        if isinstance(res, dict):
            return NoteTranslateResult(res)
        APIError(f"Translate Error: {res}", res if isinstance(res, int) else 204).raise_error()

    async def un_renote(self, *, note_id: str) -> bool:
        """Releases the note renote for the specified Id

        Parameters
        ----------
        note_id : str | None, optional
            Target note Id., by default None

        Returns
        -------
        bool
            Whether the release was successful
        """
        body = {"noteId": note_id}
        res: bool = await self._session.request(
            Route("POST", "/api/notes/unrenote"), auth=True, json=body
        )
        return res


class ClientNoteActions(SharedNoteActions):
    def __init__(
        self,
        note_id: str,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session, client)
        self._note_id: str = note_id

    @override
    async def get_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
    ) -> list[Note]:
        return await super().get_children(
            limit=limit, since_id=since_id, untilId=untilId, note_id=self._note_id
        )

    @override
    async def fetch_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
    ) -> list[Note]:
        """Get children of the note.
        update the cache of the :py:meth:`mipac.actions.note.ClientNoteActions.get_children` method

        Endpoint: `/api/notes/children`

        Parameters
        ----------
        limit : int, default=100
            limit
        since_id : str | None, default=None
            Since ID
        untilId : str | None, default=None
            Until ID

        Returns
        -------
        list[Note]
            Children of the note
        """
        return await super().fetch_children(
            limit=limit, since_id=since_id, untilId=untilId, note_id=self._note_id
        )

    @override
    async def get_all_children(
        self,
        limit: int = 10,
        since_id: str | None = None,
        untilId: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Get all children of the note

        Endpoint: `/api/notes/children`

        Parameters
        ----------
        since_id : str | None, default=None
            Since ID
        untilId : str | None, default=None
            Until ID

        Returns
        -------
        AsyncGenerator[Note, None]
            Children of the note
        """
        async for i in super().get_all_children(
            limit=limit, since_id=since_id, untilId=untilId, note_id=self._note_id
        ):
            yield i

    @override
    async def get_clips(self) -> list[Clip]:
        """Get the clips of the note

        Endpoint: `/api/notes/clips`

        Returns
        -------
        list[Clip]
            Clips of the note
        """
        return await super().get_clips(note_id=self._note_id)

    @override
    async def get_conversation(self, limit: int = 10, offset: int = 0) -> list[Note]:
        """Get the conversation of the note

        Endpoint: `/api/notes/conversation`

        Parameters
        ----------
        limit : int, default=10
            limit
        offset : int, default=0
            offset

        Returns
        -------
        list[Note]
            Notes of the conversation
        """
        return await super().get_conversation(limit=limit, offset=offset, note_id=self._note_id)

    @override
    async def delete(self) -> bool:
        """Delete a note

        Endpoint: `/api/notes/delete`

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        bool
            success or not
        """
        return await super().delete(note_id=self._note_id)

    @override
    async def get_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[NoteReaction]:
        return await super().get_reactions(
            type=type,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            note_id=self._note_id,
        )

    @override
    async def fetch_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[NoteReaction]:
        return await super().fetch_reactions(
            type=type,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            note_id=self._note_id,
        )

    @override
    async def get_renotes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[Note]:
        """Get renote of the note

        Endpoint: `/api/notes/renotes`

        Parameters
        ----------
        limit : int, default=10
            limit
        since_id : str | None, default=None
            Since ID
        until_id : str | None, default=None
            Until ID

        Returns
        -------
        list[Note]
            Renotes of the note
        """

        return await super().get_renotes(
            limit=limit, since_id=since_id, until_id=until_id, note_id=self._note_id
        )

    @override
    async def get_replies(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
    ) -> list[Note]:
        """Get replies to the note

        Endpoint: `/api/notes/replies`

        Parameters
        ----------
        since_id : str | None, default=None
            since id
        until_id : str | None, default=None
            until id
        limit : int, default=10
            limit

        Returns
        -------
        list[Note]
            replies
        """
        return await super().get_replies(
            since_id=since_id, until_id=until_id, limit=limit, note_id=self._note_id
        )

    @override
    async def get_all_replies(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
    ) -> AsyncGenerator[Note, None]:
        """Get replies to the note

        Endpoint: `/api/notes/replies`

        Parameters
        ----------
        since_id : str | None, default=None
            since id
        until_id : str | None, default=None
            until id

        Returns
        -------
        AsyncGenerator[Note, None]
            replies
        """

        async for i in super().get_all_replies(
            since_id=since_id, until_id=until_id, limit=limit, note_id=self._note_id
        ):
            yield i

    @override
    async def get_state(self) -> NoteState:
        """Get the state of the note

        Endpoint: `/api/notes/state`

        Returns
        -------
        NoteState
            Note state
        """

        return await super().get_state(note_id=self._note_id)

    @override
    async def fetch_state(self) -> NoteState:
        """Get the state of the note.

        update the cache of the :py:meth:`mipac.actions.note.ClientNoteActions.get_state` method

        Endpoint: `/api/notes/state`

        Returns
        -------
        NoteState
            Note state
        """
        return await super().fetch_state(note_id=self._note_id)

    async def add_clips(self, clip_id: str) -> bool:
        """Add a note to the clip

        Endpoint: `/api/clips/add-note`

        Parameters
        ----------
        clip_id : str
            clip id

        Returns
        -------
        bool
            success or not
        """
        return await super().add_clips(clip_id=clip_id, note_id=self._note_id)

    @override
    async def create_renote(self) -> Note:
        """Renote a note

        Endpoint: `/api/notes/create`

        Returns
        -------
        Note
            Renoted note
        """

        return await super().create_renote(note_id=self._note_id)

    @override
    async def renote(
        self,
        text: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        channel_id: str | None = None,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
    ):
        """Renote a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str | None, default=None
            text
        visibility : INoteVisibility, default='public'
            Disclosure range
        visible_user_ids : list[str] | None, default=None
            List of users to be published
        cw : str | None, default=None
            Text to be displayed when warning is given
        local_only : bool, default=False
            Whether to show only locally or not
        reaction_acceptance : IReactionAcceptance, default=None
            Reaction acceptance setting
        extract_mentions : bool, default=True
            Whether to expand the mention
        extract_hashtags : bool, default=True
            Whether to expand the hashtag
        extract_emojis : bool, default=True
            Whether to expand the emojis
        channel_id : str | None, default=None
            Channel ID
        files : list[MiFile | File | str] | None, default=None
            The ID list of files to be attached
        poll : MiPoll | None, default=None
        """

        return await super().renote(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            channel_id=channel_id,
            files=files,
            poll=poll,
            renote_id=self._note_id,
        )

    @override
    async def reply(
        self,
        text: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
    ) -> Note:
        return await super().reply(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            files=files,
            poll=poll,
            reply_id=self._note_id,
        )

    @override
    async def create_quote(
        self,
        content: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
    ) -> Note:
        """Create a note quote.

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        content: str | None, default=None
            text
        visibility: INoteVisibility, default='public'
            Disclosure range
        visible_user_ids: list[str] | None, default=None
            List of users to be published
        cw: str | None, default=None
            Text to be displayed when warning is given
        local_only: bool, default=False
            Whether to show only locally or not
        extract_mentions: bool, default=True
            Whether to expand the mention
        extract_hashtags: bool, default=True
            Whether to expand the hashtag
        extract_emojis: bool, default=True
            Whether to expand the emojis
        files: list[MiFile | File | str] | None, default=None
            The ID list of files to be attached
        poll: MiPoll | None, default=None
            Questionnaire to be created
        """

        return await super().create_quote(
            content=content,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            files=files,
            poll=poll,
            note_id=self._note_id,
        )

    @override
    async def translate(
        self,
        target_lang: str = "en-US",
    ) -> NoteTranslateResult:
        """Translate a note

        Endpoint: `/api/notes/translate`

        Parameters
        ----------
        target_lang : str, default='en'
            Target language

        Returns
        -------
        NoteTranslateResult
            Translated result
        """

        return await super().translate(target_lang=target_lang, note_id=self._note_id)

    @override
    async def un_renote(self) -> bool:
        """Releases the note renote for the specified Id

        Returns
        -------
        bool
            Whether the release was successful
        """

        return await super().un_renote(note_id=self._note_id)


class NoteActions(SharedNoteActions):
    def __init__(
        self,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)

    async def create(
        self,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance | None = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        reply_id: str | None = None,
        renote_id: str | None = None,
        channel_id: str | None = None,
        text: str | None = None,
        file_ids: list[MiFile | File | str] = MISSING,
        media_ids: list[str] = MISSING,
        poll: MiPoll | None = None,
    ) -> Note:
        data = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            reply_id=reply_id,
            renote_id=renote_id,
            channel_id=channel_id,
            files=file_ids,
            media_ids=media_ids,
            poll=poll,
        )

        raw_created_note: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            auth=True,
            json=data,
        )

        return Note(raw_note=raw_created_note["created_note"], client=self._client)

    async def get_featured(
        self, limit: int = 10, until_id: str | None = None, channel_id: str | None = None
    ):
        """Get featured notes

        Endpoint: `/api/notes/featured`

        Parameters
        ----------
        limit : int, default=10
            limit
        until_id : str | None, default=None
            Until ID
        channel_id : str | None, default=None
            channel id

        Returns
        -------
        list[Note]
            featured notes
        """
        data = {"limit": limit, "untilId": until_id, "channelId": channel_id}
        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/featured"), json=data
        )
        return [Note(note, client=self._client) for note in res]

    async def get_global_time_line(
        self,
        with_files: bool = False,
        with_renotes: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
    ):
        """Get global timeline

        Endpoint: `/api/notes/global-timeline`

        Parameters
        ----------
        with_files : bool, default=False
            Whether to include files
        with_renotes : bool, default=True
            Whether to include renote
        limit : int, default=10
            limit
        since_id : str | None, default=None
            Since ID
        until_id : str | None, default=None
            Until ID
        since_date : int | None, default=None
            Since date
        until_date : int | None, default=None
            Until date

        Returns
        -------
        list[Note]
            global timeline
        """
        data = {
            "withFiles": with_files,
            "withRenotes": with_renotes,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
        }
        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/global-timeline"), json=data
        )
        return [Note(note, client=self._client) for note in res]

    async def get_hybird_time_line(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        allow_partial: bool = False,
        include_my_rnotes: bool = True,
        include_renoted_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_files: bool = False,
        with_renotes: bool = True,
        with_replies: bool = False,
    ):
        data = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "allowPartial": allow_partial,
            "includeMyRenotes": include_my_rnotes,
            "includeRenotedMyNotes": include_renoted_my_notes,
            "includeLocalRenotes": include_local_renotes,
            "withFiles": with_files,
            "withRenotes": with_renotes,
            "withReplies": with_replies,
        }

        res = await self._session.request(
            Route("POST", "/api/notes/hybrid-timeline"), json=data, auth=True
        )

        return [Note(note, client=self._client) for note in res]

    async def get_local_timeline(
        self,
        with_files: bool = False,
        with_renotes: bool = True,
        with_replies: bool = False,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        allow_partial: bool = False,
        since_date: int | None = None,
        until_date: int | None = None,
    ):
        data = {
            "withFiles": with_files,
            "withRenotes": with_renotes,
            "withReplies": with_replies,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "allowPartial": allow_partial,
            "sinceDate": since_date,
            "untilDate": until_date,
        }

        res = await self._session.request(
            Route("POST", "/api/notes/local-timeline"), json=data, auth=True
        )

        return [Note(note, client=self._client) for note in res]

    async def get_mentions(
        self,
        following: bool = False,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        visibility: INoteVisibility = "public",
    ):
        """Get notes with mentions addressed to you

        Endpoint: `/api/notes/mentions`

        Parameters
        ----------
        following : bool, default=False
            Whether to include only users you follow
        limit : int, default=10
            limit
        since_id : str | None, default=None
            Since ID
        until_id : str | None, default=None
            Until ID
        visibility : INoteVisibility, default='public'
            Disclosure range
        """
        data = {
            "following": following,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "visibility": visibility,
        }

        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/mentions"), json=data, auth=True
        )

        return [Note(note, client=self._client) for note in res]

    async def search_by_tag(
        self,
        tag: str,
        reply: bool | None = None,
        renote: bool | None = None,
        with_files: bool | None = None,
        poll: bool | None = None,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        query: list[list[str]] | None = None,
    ):
        """Search for notes by tag

        Endpoint: `/api/notes/search-by-tag`

        Parameters
        ----------
        tag : str
            Tag to search for
        reply : bool | None, default=None
            Whether to include reply notes
        renote : bool | None, default=None
            Whether to include renote notes
        with_files : bool | None, default=None
            Whether to include notes with files
        poll : bool | None, default=None
            Whether to include notes with polls
        since_id : str | None, default=None
            ID to get notes since this ID (exclusive)
        until_id : str | None, default=None
            ID to get notes until this ID (exclusive)
        limit : int, default=10
            Maximum number of notes to retrieve
        query : list[list[str]] | None, default=None
            Additional search query

        Returns
        -------
        list[Note]
            Found notes matching the tag
        """
        data = {
            "tag": tag,
            "reply": reply,
            "renote": renote,
            "withFiles": with_files,
            "poll": poll,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "query": query,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/notes/search-by-tag"), json=data, auth=True
        )
        return [Note(raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_search_by_tag(
        self,
        tag: str,
        reply: bool | None = None,
        renote: bool | None = None,
        with_files: bool | None = None,
        poll: bool | None = None,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        query: list[list[str]] | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Search for all notes by tag using pagination

        Endpoint: `/api/notes/search-by-tag`

        Parameters
        ----------
        tag : str
            Tag to search for
        reply : bool | None, default=None
            Whether to include reply notes
        renote : bool | None, default=None
            Whether to include renote notes
        with_files : bool | None, default=None
            Whether to include notes with files
        poll : bool | None, default=None
            Whether to include notes with polls
        since_id : str | None, default=None
            ID to get notes since this ID (exclusive)
        until_id : str | None, default=None
            ID to get notes until this ID (exclusive)
        limit : int, default=10
            Maximum number of notes per request
        query : list[list[str]] | None, default=None
            Additional search query

        Returns
        -------
        AsyncGenerator[Note, None]
            Found notes matching the tag
        """
        data = {
            "tag": tag,
            "reply": reply,
            "renote": renote,
            "withFiles": with_files,
            "poll": poll,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "query": query,
        }

        pagination = Pagination[INote](
            http_client=self._session, route=Route("POST", "/api/notes/search-by-tag"), json=data
        )

        while pagination.is_final is False:
            raw_notes: list[INote] = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note, client=self._client)

    async def search(
        self,
        query: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        offset: int = 0,
        host: str | None = None,
        user_id: str | None = None,
        channel_id: str | None = None,
    ):  # Implement methods for each ID in actions
        """Search for notes

        Endpoint: `/api/notes/search`

        Parameters
        ----------
        query : str
            Search query string
        since_id : str | None, default=None
            ID to get notes since this ID (exclusive)
        until_id : str | None, default=None
            ID to get notes until this ID (exclusive)
        limit : int, default=10
            Maximum number of notes to retrieve
        offset : int, default=0
            Offset for pagination
        host : str | None, default=None
            Target server hostname
            Use "." for localhost
        user_id : str | None, default=None
            Target user ID to search within
        channel_id : str | None, default=None
            Target channel ID to search within

        Returns
        -------
        list[Note]
            Search results
        """
        body = {
            "query": query,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "offset": offset,
            "host": host,
            "userId": user_id,
            "channelId": channel_id,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/notes/search"), json=body
        )

        return [Note(raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_search(
        self,
        query: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        offset: int = 0,
        host: str | None = None,
        user_id: str | None = None,
        channel_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Search for all notes using pagination

        Endpoint: `/api/notes/search`

        Parameters
        ----------
        query : str
            Search query string
        since_id : str | None, default=None
            ID to get notes since this ID (exclusive)
        until_id : str | None, default=None
            ID to get notes until this ID (exclusive)
        limit : int, default=10
            Maximum number of notes per request
        offset : int, default=0
            Offset for pagination
        host : str | None, default=None
            Target server hostname
            Use "." for localhost
        user_id : str | None, default=None
            Target user ID to search within
        channel_id : str | None, default=None
            Target channel ID to search within

        Returns
        -------
        AsyncGenerator[Note, None]
            Search results
        """
        body = {
            "query": query,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "offset": offset,
            "host": host,
            "userId": user_id,
            "channelId": channel_id,
        }

        pagination = Pagination[INote](
            http_client=self._session, route=Route("POST", "/api/notes/search"), json=body
        )

        while pagination.is_final is False:
            raw_notes: list[INote] = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note, client=self._client)

    @deprecated
    async def send(
        self,
        text: str | None = None,
        visibility: INoteVisibility = MISSING,
        visible_user_ids: list[str] = MISSING,
        cw: str | None = None,
        local_only: bool = MISSING,
        reaction_acceptance: IReactionAcceptance = None,
        no_extract_mentions: bool = MISSING,
        no_extract_hashtags: bool = MISSING,
        no_extract_emojis: bool = MISSING,
        reply_id: str | None = None,
        renote_id: str | None = None,
        channel_id: str | None = None,
        files: list[MiFile | File | str] = MISSING,
        poll: MiPoll | None = None,
    ) -> Note:
        """Send a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str | None, default=None
            Content to post
        visibility : INoteVisibility, optional
            Visibility scope, by default "public"
            Enum: "public" "home" "followers" "specified"
        visible_user_ids : list[str] | None, optional
            Users to share with (for "specified" visibility), by default None
        cw : str | None, optional
            Content warning text, by default None
        local_only : bool, optional
            Whether to display only locally, by default False
        reaction_acceptance : IReactionAcceptance, optional
            Reaction acceptance settings, by default None
        extract_mentions : bool, optional
            Whether to extract mentions, by default True
        extract_hashtags : bool, optional
            Whether to extract hashtags, by default True
        extract_emojis : bool, optional
            Whether to extract emojis, by default True
        reply_id : str | None, optional
            ID of the note to reply to, by default None
        renote_id : str | None, optional
            ID of the note to renote, by default None
        channel_id : str | None, optional
            Channel ID, by default None
        files : list[MiFile | File | str], optional
            List of files to attach, by default None
        poll : MiPoll | None, optional
            Poll data, by default None

        Returns
        -------
        Note
            The posted note

        Raises
        ------
        ContentRequired
            When no content is provided
        """
        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            reply_id=reply_id,
            renote_id=renote_id,
            channel_id=channel_id,
            files=files,
            poll=poll,
        )
        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            auth=True,
            lower=True,
        )
        return Note(res["created_note"], client=self._client)

    @cache(group="get_note")
    async def get(self, note_id: str) -> Note:
        """Get a note

        Endpoint: `/api/notes/show`

        Parameters
        ----------
        note_id : str
            Note ID

        Returns
        -------
        Note
            Retrieved note
        """
        raw_note: INote = await self._session.request(
            Route("POST", "/api/notes/show"),
            json={"noteId": note_id},
            auth=True,
            lower=True,
        )
        return Note(raw_note=raw_note, client=self._client)

    @cache(group="get_note", override=True)
    async def fetch(self, note_id: str) -> Note:
        """Get a note.

        update the cache of the :py:meth:`mipac.actions.note.NoteActions.get` method

        Endpoint: `/api/notes/show`

        Parameters
        ----------
        note_id : str
            note id

        Returns
        -------
        Note
            note
        """
        raw_note: INote = await self._session.request(
            Route("POST", "/api/notes/show"),
            json={"noteId": note_id},
            auth=True,
            lower=True,
        )
        return Note(raw_note=raw_note, client=self._client)

    async def gets(
        self,
        local: bool = False,
        reply: bool = False,
        renote: bool = False,
        with_files: bool = False,
        poll: bool = False,
        limit: int = 100,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[Note, None]:
        if limit > 100:
            raise ValueError("limit must be 100 or less")

        if get_all:
            limit = 100

        body = remove_dict_empty(
            {
                "local": local,
                "reply": reply,
                "renote": renote,
                "withFiles": with_files,
                "poll": poll,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
            }
        )

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/notes"), json=body, limit=limit
        )

        while pagination.is_final is False:
            raw_notes = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note=raw_note, client=self._client)

    async def get_time_line(
        self,
        list_id: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
    ) -> list[Note]:
        """
        Get the timeline of the specified list

        Endpoint: `/api/notes/user-list-timeline`

        Parameters
        ----------
        list_id : str
            List ID
        limit : int, default=10
            limit
        since_id : str | None, default=None
            Since ID
        until_id : str | None, default=None
            Until ID
        since_date : int | None, default=None
            Since date
        until_date : int | None, default=None
            Until date
        include_renote_my_notes : bool, default=True
            Whether to include your own renote
        include_local_renotes : bool, default=True
            Whether to include local renote
        with_renotes : bool, default=True
            Whether to include renote
        with_files : bool, default=True
            Whether to include files

        Returns
        -------
        list[Note]

        Notes
        -----
        """
        data = {
            "limit": limit,
            "listId": list_id,
            "includeRenoteMyNotes": include_renote_my_notes,
            "includeLocalRenotes": include_local_renotes,
            "withRenotes": with_renotes,
            "withFiles": with_files,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/notes/user-list-timeline"), json=data, auth=True
        )

        return [Note(raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_time_line(
        self,
        list_id: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        include_renote_my_notes: bool = True,
        include_local_renotes: bool = True,
        with_renotes: bool = True,
        with_files: bool = True,
    ):
        data = {
            "limit": limit,
            "listId": list_id,
            "includeRenoteMyNotes": include_renote_my_notes,
            "includeLocalRenotes": include_local_renotes,
            "withRenotes": with_renotes,
            "withFiles": with_files,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
        }

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/notes/user-list-timeline"), json=data, auth=True
        )

        while pagination.is_final is False:
            raw_notes: list[INote] = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note, client=self._client)
