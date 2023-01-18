from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import APIError, ParameterError
from mipac.file import MiFile
from mipac.http import HTTPClient, Route
from mipac.models.drive import File
from mipac.models.note import (
    Note,
    NoteReaction,
    NoteState,
    NoteTranslateResult,
)
from mipac.models.poll import MiPoll, Poll
from mipac.types.note import (
    ICreatedNote,
    INote,
    INoteState,
    INoteTranslateResult,
)
from mipac.util import cache, check_multi_arg, remove_dict_empty

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ['NoteActions']


def create_note_body(
    content: str | None = None,
    visibility: str = 'public',
    visible_user_ids: list[str] | None = None,
    cw: str | None = None,
    local_only: bool = False,
    extract_mentions: bool = True,
    extract_hashtags: bool = True,
    extract_emojis: bool = True,
    reply_id: str | None = None,
    renote_id: str | None = None,
    channel_id: str | None = None,
    files: list[MiFile | File | str] | None = None,
    poll: MiPoll | None = None,
):
    body = {
        'visibility': visibility,
        'visibleUserIds': visible_user_ids,
        'text': content,
        'cw': cw,
        'localOnly': local_only,
        'noExtractMentions': not extract_mentions,
        'noExtractHashtags': not extract_hashtags,
        'noExtractEmojis': not extract_emojis,
        'replyId': reply_id,
        'renoteId': renote_id,
        'channelId': channel_id,
    }
    if not check_multi_arg(content, files, renote_id, poll):
        raise ParameterError(
            'ノートの送信にはcontent, file_ids, renote_id またはpollのいずれか1つが無くてはいけません'
        )

    if poll and type(Poll):
        poll_data = remove_dict_empty(
            {
                'choices': poll.choices,
                'multiple': poll.multiple,
                'expiresAt': poll.expires_at,
                'expiredAfter': poll.expired_after,
            }
        )
        body['poll'] = poll_data
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
                raise ParameterError('files must be MiFile or str or File')
        body['fileIds'] = file_ids

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

    async def un_renote(self, note_id: str | None = None) -> bool:
        """
        Releases the note renote for the specified Id

        Parameters
        ----------
        note_id : str | None, optional
            Target note Id., by default None

        Returns
        -------
        bool
            Whether the release was successful
        """

        body = {'noteId': note_id}
        res: bool = await self._session.request(
            Route('POST', '/api/notes/unrenote'), auth=True, json=body
        )
        return res

    async def get_children(
        self,
        limit: int = 100,
        since_id: str | None = None,
        untilId: str | None = None,
        note_id: str | None = None,
        all: bool = True,
    ) -> AsyncIterator[Note]:

        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        async def request(body) -> list[Note]:
            res: list[INote] = await self._session.request(
                Route('POST', '/api/notes/children'),
                lower=True,
                auth=True,
                json=body,
            )
            return [Note(note, client=self._client) for note in res]

        note_id = note_id or self._note_id
        data = {
            'noteId': note_id,
            'limit': limit,
            'sinceId': since_id,
            'untilId': untilId,
        }
        first_req = await request(data)
        for note in first_req:
            yield note

        if all and len(first_req) == 100:
            data['untilId'] = first_req[-1].id
            while True:
                res = await request(data)
                if len(res) <= 100:
                    for note in res:
                        yield note
                if len(res) == 0:
                    break
                data['untilId'] = res[-1].id

    async def get_state(self, note_id: str | None = None) -> NoteState:
        note_id = note_id or self._note_id
        data = {'noteId': note_id}
        res: INoteState = await self._session.request(
            Route('POST', '/api/notes/state'), auth=True, json=data
        )
        return NoteState(res)

    async def add_clips(
        self, clip_id: str, note_id: str | None = None
    ) -> bool:
        """
        クリップに追加します

        Parameters
        ----------
        note_id : str | None, default=None
                追加するノートのID
        clip_id : str
            クリップのID
        note_id : str | None, default=None
            追加したいノートのID

        Returns
        -------
        bool
            成功したか否か
        """

        note_id = note_id or self._note_id

        data = {'noteId': note_id, 'clipId': clip_id}
        return bool(
            await self._session.request(
                Route('POST', '/api/clips/add-note'), json=data, auth=True
            )
        )

    async def delete(self, note_id: str | None = None) -> bool:
        """
        Delete a note

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

        data = {'noteId': note_id}
        res = await self._session.request(
            Route('POST', '/api/notes/delete'), json=data, auth=True
        )
        return bool(res)

    async def create_renote(self, note_id: str | None = None) -> Note:
        """
        Renote a note

        Parameters
        ----------
        note_id : str | None, default=None
            note id

        Returns
        -------
        Note
            Renoted note
        """
        body = create_note_body(renote_id=note_id,)
        res: ICreatedNote = await self._session.request(
            Route('POST', '/api/notes/create'),
            json=body,
            auth=True,
            lower=True,
        )
        return Note(res['created_note'], client=self._client)

    async def get_reaction(
        self, reaction: str, note_id: str | None = None
    ) -> list[NoteReaction]:
        note_id = note_id or self._note_id
        return await self._client.note.reaction.action.get_reaction(
            reaction
        )  # TODO: note.reactionのインタンスを新規作成出来るように

    async def reply(
        self,
        content: str | None = None,
        visibility: str = 'public',
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        reply_id: str | None = None,
    ) -> Note:

        reply_id = reply_id or self._note_id

        body = create_note_body(
            content=content,
            cw=cw,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            extract_emojis=extract_emojis,
            extract_hashtags=extract_hashtags,
            extract_mentions=extract_mentions,
            poll=poll,
            local_only=local_only,
            reply_id=reply_id,
            files=files,
        )
        res: ICreatedNote = await self._session.request(
            Route('POST', '/api/notes/create'),
            json=body,
            lower=True,
            auth=True,
        )
        return Note(res['created_note'], client=self._client)

    async def create_quote(
        self,
        content: str | None = None,
        visibility: str = 'public',
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        note_id: str | None = None,
    ) -> Note:
        """
        Create a note quote.

        Parameters
        ----------
        content: str | None, default=None
            text
        visibility: str, default='public'
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

        body = create_note_body(
            content=content,
            cw=cw,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            extract_emojis=extract_emojis,
            extract_hashtags=extract_hashtags,
            extract_mentions=extract_mentions,
            poll=poll,
            local_only=local_only,
            renote_id=note_id,
            files=files,
        )
        res: ICreatedNote = await self._session.request(
            Route('POST', '/api/notes/create'),
            json=body,
            auth=True,
            lower=True,
        )

        return Note(res['created_note'], client=self._client)

    @cache(group='translate_note')
    async def translate(
        self, note_id: str | None = None, target_lang: str = 'en-US',
    ) -> NoteTranslateResult:
        """
        Translate a note

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

        data = {'noteId': note_id, 'targetLang': target_lang}
        res: INoteTranslateResult = await self._session.request(
            Route('POST', '/api/notes/translate'), json=data, auth=True
        )
        if isinstance(res, dict):
            return NoteTranslateResult(res)
        APIError(
            f'Translate Error: {res}', res if isinstance(res, int) else 204
        ).raise_error()


class NoteActions(ClientNoteActions):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):

        super().__init__(note_id=note_id, session=session, client=client)

    async def send(
        self,
        content: str | None = None,
        visibility: str = 'public',
        visible_user_ids: list[str] | None = None,
        cw: str | None = None,
        local_only: bool = False,
        extract_mentions: bool = True,
        extract_hashtags: bool = True,
        extract_emojis: bool = True,
        reply_id: str | None = None,
        renote_id: str | None = None,
        channel_id: str | None = None,
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
    ) -> Note:
        """
        ノートを投稿します。

        Parameters
        ----------
        content : str | None, default=None
            投稿する内容
        visibility : str, optional
            公開範囲, by default "public"
            Enum: "public" "home" "followers" "specified"
        visible_user_ids : list[str] | None, optional
            公開するユーザー, by default None
        cw : str | None, optional
            閲覧注意の文字, by default None
        local_only : bool, optional
            ローカルにのみ表示するか, by default False
        extract_mentions : bool, optional
            メンションを展開するか, by default False
        extract_hashtags : bool, optional
            ハッシュタグを展開するか, by default False
        extract_emojis : bool, optional
            絵文字を展開するか, by default False
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
            content=content,
            cw=cw,
            channel_id=channel_id,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            extract_emojis=extract_emojis,
            extract_hashtags=extract_hashtags,
            extract_mentions=extract_mentions,
            files=files,
            poll=poll,
            local_only=local_only,
            renote_id=renote_id,
            reply_id=reply_id,
        )
        res: ICreatedNote = await self._session.request(
            Route('POST', '/api/notes/create'),
            json=body,
            auth=True,
            lower=True,
        )
        return Note(res['created_note'], client=self._client)

    @cache(group='get_note')
    async def get(self, note_id: str | None = None) -> Note:
        """
        ノートを取得します

        Parameters
        ----------
        note_id : str | None, default=None
            ノートのID

        Returns
        -------
        Note
            取得したノートID
        """
        note_id = note_id or self._note_id
        res = await self._session.request(
            Route('POST', '/api/notes/show'),
            json={'noteId': note_id},
            auth=True,
            lower=True,
        )
        return Note(res, client=self._client)

    @cache(group='get_note', override=True)
    async def fetch(self, note_id: str | None = None) -> Note:
        note_id = note_id or self._note_id
        res = await self._session.request(
            Route('POST', '/api/notes/show'),
            json={'noteId': note_id},
            auth=True,
            lower=True,
        )
        return Note(res, client=self._client)

    async def get_replies(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        note_id: str | None = None,
    ) -> list[Note]:
        """
        ノートに対する返信を取得します

        Parameters
        ---------
        since_id : str | None, default=None
            指定すると、その投稿を投稿を起点としてより新しい投稿を取得します
        until_id : str | None, default=None
            指定すると、その投稿を投稿を起点としてより古い投稿を取得します
        limit : int, default=10
            取得する上限
        note_id: str | None, default=None
            返信を取得したいノートのID

        Returns
        -------
        list[Note]
            返信のリスト
        """
        note_id = note_id or self._note_id
        res = await self._session.request(
            Route('POST', '/api/notes/replies'),
            json={
                'noteId': note_id,
                'sinceId': since_id,
                'untilId': until_id,
                'limit': limit,
            },
            auth=True,
            lower=True,
        )
        return [Note(i, client=self._client) for i in res]

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
        all: bool = False,
    ) -> AsyncIterator[Note]:

        if limit > 100:
            raise ParameterError('limit は100以下である必要があります')

        async def request(body) -> list[Note]:
            res: list[INote] = await self._session.request(
                Route('POST', '/api/notes'), lower=True, auth=True, json=body
            )
            return [Note(note, client=self._client) for note in res]

        body = remove_dict_empty(
            {
                'local': local,
                'reply': reply,
                'renote': renote,
                'withFiles': with_files,
                'poll': poll,
                'limit': limit,
                'sinceId': since_id,
                'untilId': until_id,
            }
        )

        if all:
            body['limit'] = 100
        first_req = await request(body)

        for note in first_req:
            yield note

        if all and len(first_req) == 100:
            body['untilId'] = first_req[-1].id
            while True:
                res = await request(body)
                if len(res) <= 100:
                    for note in res:
                        yield note
                if len(res) == 0:
                    break
                body['untilId'] = res[-1].id
