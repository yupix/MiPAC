from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.errors.base import APIError, ParameterError
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
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination
from mipac.utils.util import check_multi_arg, deprecated

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ["NoteActions"]


def create_note_body(
    text: str | None = None,
    visibility: INoteVisibility = "public",
    visible_user_ids: list[str] | None = None,
    cw: str | None = None,
    local_only: bool = False,
    reaction_acceptance: IReactionAcceptance = None,
    extract_mentions: bool = True,
    extract_hashtags: bool = True,
    extract_emojis: bool = True,
    reply_id: str | None = None,
    renote_id: str | None = None,
    channel_id: str | None = None,
    files: list[MiFile | File | str] | None = None,
    media_ids: list[str] | None = None,
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
        "noExtractMentions": not extract_mentions,
        "noExtractHashtags": not extract_hashtags,
        "noExtractEmojis": not extract_emojis,
        "replyId": reply_id,
        "renoteId": renote_id,
        "channelId": channel_id,
    }
    if not check_multi_arg(text, files, renote_id, poll):
        raise ParameterError(
            "To send a note, one of content, file_ids, renote_id or poll is required"
        )

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
    if files:
        file_ids = []
        for file in files:
            if isinstance(file, MiFile):
                file_ids.append(file.file_id)
            elif isinstance(file, File):
                file_ids.append(file.id)
            elif isinstance(file, str):
                file_ids.append(file)
            else:
                raise ParameterError("files must be MiFile or str or File")
        body["fileIds"] = file_ids

    return remove_dict_empty(body)


class ClientNoteActions(AbstractAction):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        self._note_id: str | None = note_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @cache(group="get_note_children")
    async def get_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
        note_id: str | None = None,
    ) -> list[Note]:
        if limit > 100:
            raise ParameterError("limit は100以下である必要があります")

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

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

    @cache(group="get_note_children", override=True)
    async def fetch_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
        note_id: str | None = None,
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
        note_id = note_id or self._note_id
        return await self.get_children(
            limit=limit, since_id=since_id, untilId=untilId, note_id=note_id
        )

    async def get_all_children(
        self,
        since_id: str | None = None,
        untilId: str | None = None,
        note_id: str | None = None,
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
        limit = 100

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

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

    async def get_clips(self, note_id: str | None = None) -> list[Clip]:
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

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id}
        res: list[IClip] = await self._session.request(
            Route("POST", "/api/notes/clips"), json=data, auth=True
        )
        return [Clip(clip, client=self._client) for clip in res]

    async def get_conversation(
        self, limit: int = 10, offset: int = 0, *, note_id: str | None = None
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
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id, "limit": limit, "offset": offset}
        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/conversation"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    async def delete(self, *, note_id: str | None = None) -> bool:
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

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id}
        res = await self._session.request(Route("POST", "/api/notes/delete"), json=data, auth=True)
        return bool(res)

    @cache(group="get_note_state")
    async def get_state(self, note_id: str | None = None) -> NoteState:
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
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id}
        res: INoteState = await self._session.request(
            Route("POST", "/api/notes/state"), auth=True, json=data
        )
        return NoteState(res)

    @cache(group="get_note_state", override=True)
    async def fetch_state(self, note_id: str | None = None) -> NoteState:
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
        note_id = note_id or self._note_id
        return await self.get_state(note_id=note_id)

    async def add_clips(self, clip_id: str, note_id: str | None = None) -> bool:
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

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id, "clipId": clip_id}
        return bool(
            await self._session.request(Route("POST", "/api/clips/add-note"), json=data, auth=True)
        )

    async def create_renote(self, note_id: str | None = None) -> Note:
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

        note_id = self._note_id or note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        body = create_note_body(renote_id=note_id)
        res: ICreatedNote = await self._session.request(
            Route("POST", "/api/notes/create"),
            json=body,
            auth=True,
            lower=True,
        )
        return Note(res["created_note"], client=self._client)

    async def get_reactions(
        self,
        reaction: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str | None = None,
    ) -> list[NoteReaction]:
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        return await self._client.note.reaction.action.get_reactions(
            reaction=reaction, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )

    async def fetch_reactions(
        self,
        note_id: str | None = None,
        reaction: str | None = None,
        *,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[NoteReaction]:
        return await self._client.note.reaction.action.fetch_reactions(
            note_id=note_id, reaction=reaction, limit=limit, since_id=since_id, until_id=until_id
        )

    async def renote(
        self,
        text: str | None = None,
        visibility: INoteVisibility = "public",
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        reaction_acceptance: IReactionAcceptance = None,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        channel_id: str | None = None,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        *,
        renote_id: str | None = None,
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
        renote_id = renote_id or self._note_id

        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
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
        visibility: INoteVisibility = "public",
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        reaction_acceptance: IReactionAcceptance = None,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        reply_id: str | None = None,
    ) -> Note:
        reply_id = reply_id or self._note_id

        if reply_id is None:
            raise ParameterError("reply_id is required")

        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
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
        visibility: INoteVisibility = "public",
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        reaction_acceptance: IReactionAcceptance = None,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        note_id: str | None = None,
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

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        body = create_note_body(
            text=content,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
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
        note_id: str | None = None,
        target_lang: str = "en-US",
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
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id, "targetLang": target_lang}
        res: INoteTranslateResult = await self._session.request(
            Route("POST", "/api/notes/translate"), json=data, auth=True
        )
        if isinstance(res, dict):
            return NoteTranslateResult(res)
        APIError(f"Translate Error: {res}", res if isinstance(res, int) else 204).raise_error()

    async def get_renotes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str | None = None,
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
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

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
        note_id: str | None = None,
    ) -> list[Note]:
        """Get replies to the note

        Endpoint: `/api/notes/replies`

        Parameters
        ---------
        since_id : str | None, default=None
            since id
        until_id : str | None, default=None
            until id
        limit : int, default=10
            limit
        note_id: str | None, default=None
            note id

        Returns
        -------
        list[Note]
            replies
        """
        note_id = note_id or self._note_id

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
        note_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Get replies to the note

        Endpoint: `/api/notes/replies`

        Parameters
        ---------
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

        limit = 100

        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        body = {"noteId": note_id, "sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/notes/replies"), json=body
        )

        while True:
            res_notes = await pagination.next()
            for res_note in res_notes:
                yield Note(res_note, client=self._client)

            if pagination.is_final:
                break

    async def un_renote(self, note_id: str | None = None) -> bool:
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
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        body = {"noteId": note_id}
        res: bool = await self._session.request(
            Route("POST", "/api/notes/unrenote"), auth=True, json=body
        )
        return res


class NoteActions(ClientNoteActions):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(note_id=note_id, session=session, client=client)

    async def create(
        self,
        visibility: INoteVisibility = "public",
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        reaction_acceptance: IReactionAcceptance | None = None,
        no_extrace_mentions: bool = False,
        no_extract_hashtags: bool = False,
        no_extract_emojis: bool = False,
        reply_id: str | None = None,
        renote_id: str | None = None,
        channel_id: str | None = None,
        text: str | None = None,
        file_ids: list[MiFile | File | str] | None = None,
        media_ids: list[str] | None = None,
        poll: MiPoll | None = None,
    ) -> Note:
        data = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=not no_extrace_mentions,
            extract_hashtags=not no_extract_hashtags,
            extract_emojis=not no_extract_emojis,
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

    @override
    async def get_children(
        self,
        note_id: str,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
    ) -> list[Note]:
        return await super().get_children(
            note_id=note_id, limit=limit, since_id=since_id, untilId=untilId
        )

    @override
    async def fetch_children(
        self,
        note_id: str,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
    ) -> list[Note]:
        return await super().fetch_children(
            note_id=note_id, limit=limit, since_id=since_id, untilId=untilId
        )

    @override
    async def get_all_children(
        self, note_id: str, since_id: str | None = None, untilId: str | None = None
    ) -> AsyncGenerator[Note, None] | list[Note]:
        async for i in super().get_all_children(
            note_id=note_id, since_id=since_id, untilId=untilId
        ):
            yield i

    @override
    async def get_clips(self, note_id: str) -> list[Clip]:
        return await super().get_clips(note_id=note_id)

    @override
    async def get_conversation(self, note_id: str, limit: int = 10, offset: int = 0) -> list[Note]:
        return await super().get_conversation(note_id=note_id, limit=limit, offset=offset)

    @override
    async def delete(self, note_id: str) -> bool:
        return await super().delete(note_id=note_id)

    @deprecated
    async def send(
        self,
        text: str | None = None,
        visibility: INoteVisibility = "public",
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        reaction_acceptance: IReactionAcceptance = None,
        extract_mentions: bool = True,  # 元は noExtractMentions
        extract_hashtags: bool = True,  # 元は noExtractHashtags
        extract_emojis: bool = True,  # 元は noExtractEmojis
        reply_id: str | None = None,
        renote_id: str | None = None,
        channel_id: str | None = None,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
    ) -> Note:
        """Send a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str | None, default=None
            投稿する内容
        visibility : INoteVisibility, optional
            公開範囲, by default "public"
            Enum: "public" "home" "followers" "specified"
        visible_user_ids : list[str] | None, optional
            公開するユーザー, by default None
        cw : str | None, optional
            閲覧注意の文字, by default None
        local_only : bool, optional
            ローカルにのみ表示するか, by default False
        reaction_acceptance : IReactionAcceptance, optional
            リアクションの受け入れ設定, by default None
        extract_mentions : bool, optional
            メンションを展開するか, by default True
        extract_hashtags : bool, optional
            ハッシュタグを展開するか, by default True
        extract_emojis : bool, optional
            絵文字を展開するか, by default True
        reply_id : str | None, optional
            リプライ先のid, by default None
        renote_id : str | None, optional
            リノート先のid, by default None
        channel_id : str | None, optional
            チャンネルid, by default None
        files : list[MiFile | File | str], optional
            添付するファイルのリスト, by default None
        poll : MiPoll | None, optional
            アンケート, by default None

        Returns
        -------
        Note
            投稿したノート

        Raises
        ------
        ContentRequired
            [description]
        """
        body = create_note_body(
            text=text,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            cw=cw,
            local_only=local_only,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
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
            ノートのID

        Returns
        -------
        Note
            取得したノートID
        """
        res = await self._session.request(
            Route("POST", "/api/notes/show"),
            json={"noteId": note_id},
            auth=True,
            lower=True,
        )
        return Note(res, client=self._client)

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
        res = await self._session.request(
            Route("POST", "/api/notes/show"),
            json={"noteId": note_id},
            auth=True,
            lower=True,
        )
        return Note(res, client=self._client)

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
            raise ParameterError("limit は100以下である必要があります")

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

        while True:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self._client)
            if get_all is False or pagination.is_final:
                break

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
