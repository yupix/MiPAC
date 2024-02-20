from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, override

from mipac.abstract.action import AbstractAction
from mipac.file import MiFile
from mipac.http import HTTPClient, Route
from mipac.models.channel import Channel
from mipac.models.drive import File
from mipac.models.note import Note
from mipac.models.poll import MiPoll
from mipac.types.channel import IChannel
from mipac.types.note import INote, INoteVisibility
from mipac.types.reaction import IReactionAcceptance
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedChannelActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

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
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        *,
        channel_id: str,
    ) -> Note:
        """Send a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str, optional
            Text of the note, by default None
        visibility : INoteVisibility, optional
            Visibility of the note, by default "public"
        visible_user_ids : list[str], optional
            Visible user IDs, by default None
        cw : str, optional
            CW of the note, by default None
        local_only : bool, optional
            Whether the note is local only, by default False
        reaction_acceptance : IReactionAcceptance, optional
            Reaction acceptance of the note, by default None
        extract_mentions : bool, optional
            Whether to extract mentions, by default True
        extract_hashtags : bool, optional
            Whether to extract hashtags, by default True
        extract_emojis : bool, optional
            Whether to extract emojis, by default True
        reply_id : str, optional
            Reply ID, by default None
        renote_id : str, optional
            Renote ID, by default None
        files : list[MiFile | File | str], optional
            Files, by default None
        poll : MiPoll, optional
            Poll, by default None
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        Note
            Created note
        """
        return await self._client.note.action.send(
            text=text,
            cw=cw,
            files=files,
            poll=poll,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
            reply_id=reply_id,
            renote_id=renote_id,
            channel_id=channel_id,
            local_only=local_only,
        )

    async def follow(self, *, channel_id: str) -> bool:
        """Follow a channel

        Endpoint: `/api/channels/follow`

        Parameters
        ----------
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        bool
            Whether the channel is followed
        """
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/follow"), json=data, auth=True, lower=True
        )
        return res

    async def unfollow(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルのフォローを解除します

        Endpoint: `/api/channels/unfollow`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            フォロー解除に成功したかどうか
        """
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/unfollow"), json=data, auth=True, lower=True
        )
        return res

    async def update(
        self,
        name: str | None = MISSING,
        description: str | None = MISSING,
        banner_id: str | None = MISSING,
        is_archived: bool | None = MISSING,
        pinned_note_ids: list[str] | None = MISSING,
        color: str | None = MISSING,
        is_sensitive: bool | None = MISSING,
        allow_renote_to_external: bool | None = MISSING,
        *,
        channel_id: str,
    ) -> Channel:
        """チャンネルの情報を更新します

        Endpoint: `/api/channels/update`

        Parameters
        ----------
        name : str | None
            チャンネル名, default=MISSING
        description : str | None
            チャンネルの説明, default=MISSING
        banner_id : str | None
            バナー画像のID, default=MISSING
        is_archived : bool | None
            チャンネルがアーカイブされているかどうか, default=MISSING
        pinned_note_ids : list[str] | None
            ピン留めするノートのIDリスト, default=MISSING
        color : str | None
            チャンネルの色, default=MISSING
        is_sensitive : bool | None
            チャンネルがセンシティブかどうか, default=MISSING
        allow_renote_to_external : bool | None
            外部へのリノートを許可するかどうか, default=MISSING
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        Channel
            更新後のチャンネル
        """
        data = remove_dict_missing(
            {
                "channelId": channel_id,
                "name": name,
                "description": description,
                "bannerId": banner_id,
                "isArchived": is_archived,
                "pinnedNoteIds": pinned_note_ids,
                "color": color,
                "isSensitive": is_sensitive,
                "allowRenoteToExternal": allow_renote_to_external,
            }
        )
        raw_channel: IChannel = await self._session.request(
            Route("POST", "/api/channels/update"), json=data, auth=True, remove_none=False
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    async def timeline(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        *,
        channel_id: str,
    ) -> list[Note]:
        """チャンネルのタイムラインを取得します

        Endpoint: `/api/channels/timeline`

        Parameters
        ----------
        limit : int
            一度に取得する件数, default=10
        since_id : str | None
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None
            指定したIDのノートより前のノートを取得します, default=None
        since_date : int | None
            指定した日付のノートより後のノートを取得します, default=None
        until_date : int | None
            指定した日付のノートより前のノートを取得します, default=None
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        list[Note]
            取得したノートのリスト
        """
        if channel_id is None:
            raise ValueError("channel_id is required")

        data = {
            "channelId": channel_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/channels/timeline"), json=data, auth=True, lower=True
        )
        return [Note(raw_note=raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_timeline(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        *,
        channel_id: str,
    ) -> AsyncGenerator[Note, None]:
        """チャンネルのタイムラインを全て取得します

        Endpoint: `/api/channels/timeline`

        Parameters
        ----------
        limit : int
            一度に取得する件数, default=10
        since_id : str | None
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None
            指定したIDのノートより前のノートを取得します, default=None
        since_date : int | None
            指定した日付のノートより後のノートを取得します, default=None
        until_date : int | None
            指定した日付のノートより前のノートを取得します, default=None
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        AsyncGenerator[Note, None]
            取得したノートのリスト
        """
        data = {
            "channelId": channel_id,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_date,
            "untilDate": until_date,
        }
        pagination = Pagination[INote](
            self._session, Route("POST", "/api/channels/timeline"), auth=True, json=data
        )

        while pagination.is_final is False:
            raw_notes: list[INote] = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note=raw_note, client=self._client)

    async def favorite(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルをお気に入りにします

        Endpoint: `/api/channels/favorite`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            お気に入りに追加できたかどうか
        """
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/favorite"), json=data, auth=True, lower=True
        )
        return res

    async def unfavorite(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルをお気に入りから外します

        Endpoint: `/api/channels/unfavorite`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            お気に入りから外せたかどうか
        """
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/unfavorite"), json=data, auth=True, lower=True
        )
        return res


class ClientChannelActions(SharedChannelActions):
    def __init__(self, channel_id: str, *, session: HTTPClient, client: ClientManager):
        self._channel_id: str = channel_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @override
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
        files: list[MiFile | File | str] | None = None,
        poll: MiPoll | None = None,
        *,
        channel_id: str | None = None,
    ) -> Note:
        """Send a note

        Endpoint: `/api/notes/create`

        Parameters
        ----------
        text : str, optional
            Text of the note, by default None
        visibility : INoteVisibility, optional
            Visibility of the note, by default "public"
        visible_user_ids : list[str], optional
            Visible user IDs, by default None
        cw : str, optional
            CW of the note, by default None
        local_only : bool, optional
            Whether the note is local only, by default False
        reaction_acceptance : IReactionAcceptance, optional
            Reaction acceptance of the note, by default None
        extract_mentions : bool, optional
            Whether to extract mentions, by default True
        extract_hashtags : bool, optional
            Whether to extract hashtags, by default True
        extract_emojis : bool, optional
            Whether to extract emojis, by default True
        reply_id : str, optional
            Reply ID, by default None
        renote_id : str, optional
            Renote ID, by default None
        files : list[MiFile | File | str], optional
            Files, by default None
        poll : MiPoll, optional
            Poll, by default None
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        Note
            Created note
        """
        channel_id = channel_id or self._channel_id
        return await super().send(
            text=text,
            cw=cw,
            files=files,
            poll=poll,
            visibility=visibility,
            visible_user_ids=visible_user_ids,
            reaction_acceptance=reaction_acceptance,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
            reply_id=reply_id,
            renote_id=renote_id,
            channel_id=channel_id,
            local_only=local_only,
        )

    @override
    async def follow(self, *, channel_id: str) -> bool:
        """Follow a channel

        Endpoint: `/api/channels/follow`

        Parameters
        ----------
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        bool
            Whether the channel is followed
        """
        return await super().follow(channel_id=channel_id)

    @override
    async def unfollow(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルのフォローを解除します

        Endpoint: `/api/channels/unfollow`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            フォロー解除に成功したかどうか
        """
        return await super().unfollow(channel_id=channel_id)

    @override
    async def update(
        self,
        name: str | None = MISSING,
        description: str | None = MISSING,
        banner_id: str | None = MISSING,
        is_archived: bool | None = MISSING,
        pinned_note_ids: list[str] | None = MISSING,
        color: str | None = MISSING,
        is_sensitive: bool | None = MISSING,
        allow_renote_to_external: bool | None = MISSING,
        *,
        channel_id: str,
    ) -> Channel:
        """チャンネルの情報を更新します

        Endpoint: `/api/channels/update`

        Parameters
        ----------
        name : str | None
            チャンネル名, default=MISSING
        description : str | None
            チャンネルの説明, default=MISSING
        banner_id : str | None
            バナー画像のID, default=MISSING
        is_archived : bool | None
            チャンネルがアーカイブされているかどうか, default=MISSING
        pinned_note_ids : list[str] | None
            ピン留めするノートのIDリスト, default=MISSING
        color : str | None
            チャンネルの色, default=MISSING
        is_sensitive : bool | None
            チャンネルがセンシティブかどうか, default=MISSING
        allow_renote_to_external : bool | None
            外部へのリノートを許可するかどうか, default=MISSING
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        Channel
            更新後のチャンネル
        """
        channel_id = channel_id or self._channel_id

        return await super().update(
            name=name,
            description=description,
            banner_id=banner_id,
            is_archived=is_archived,
            pinned_note_ids=pinned_note_ids,
            color=color,
            is_sensitive=is_sensitive,
            allow_renote_to_external=allow_renote_to_external,
            channel_id=channel_id,
        )

    @override
    async def timeline(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        *,
        channel_id: str,
    ) -> list[Note]:
        """チャンネルのタイムラインを取得します

        Endpoint: `/api/channels/timeline`

        Parameters
        ----------
        limit : int
            一度に取得する件数, default=10
        since_id : str | None
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None
            指定したIDのノートより前のノートを取得します, default=None
        since_date : int | None
            指定した日付のノートより後のノートを取得します, default=None
        until_date : int | None
            指定した日付のノートより前のノートを取得します, default=None
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        list[Note]
            取得したノートのリスト
        """
        channel_id = channel_id or self._channel_id

        return await super().timeline(
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            channel_id=channel_id,
        )

    @override
    async def get_all_timeline(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        *,
        channel_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """チャンネルのタイムラインを全て取得します

        Endpoint: `/api/channels/timeline`

        Parameters
        ----------
        limit : int
            一度に取得する件数, default=10
        since_id : str | None
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None
            指定したIDのノートより前のノートを取得します, default=None
        since_date : int | None
            指定した日付のノートより後のノートを取得します, default=None
        until_date : int | None
            指定した日付のノートより前のノートを取得します, default=None
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        AsyncGenerator[Note, None]
            取得したノートのリスト
        """
        channel_id = channel_id or self._channel_id

        async for i in super().get_all_timeline(
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            channel_id=channel_id,
        ):
            yield i

    @override
    async def favorite(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルをお気に入りにします

        Endpoint: `/api/channels/favorite`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            お気に入りに追加できたかどうか
        """
        channel_id = channel_id or self._channel_id

        return await super().favorite(channel_id=channel_id)

    @override
    async def unfavorite(self, *, channel_id: str) -> bool:
        """指定したIDのチャンネルをお気に入りから外します

        Endpoint: `/api/channels/unfavorite`

        Parameters
        ----------
        channel_id : str | None
            対象のチャンネルID, default=None

        Returns
        -------
        bool
            お気に入りから外せたかどうか
        """
        channel_id = channel_id or self._channel_id

        return await super().unfavorite(channel_id=channel_id)


class ChannelActions(SharedChannelActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        name: str,
        color: str = MISSING,
        description: str = MISSING,
        banner_id: str = MISSING,
        is_sensitive: bool = MISSING,
        allow_renote_to_external: bool = MISSING,
    ) -> Channel:
        """チャンネルを作成します

        Endpoint: `/api/channels/create`

        Parameters
        ----------
        name : str
            チャンネル名
        color : str
            チャンネルの色, default=MISSING
        description : str
            チャンネルの説明, default=MISSING
        banner_id : str
            チャンネルのバナーに使用するファイルのID, default=MISSING
        is_sensitive : bool
            チャンネルがセンシティブかどうか, default=MISSING
        allow_renote_to_external : bool, optional
            外部へのリノートを許可するかどうか, default=MISSING

        Returns
        -------
        Channel
            作成したチャンネル
        """
        data = remove_dict_missing(
            {
                "name": name,
                "color": color,
                "description": description,
                "banner_id": banner_id,
                "is_sensitive": is_sensitive,
                "allow_renote_to_external": allow_renote_to_external,
            }
        )
        raw_channel: IChannel = await self._session.request(
            Route("POST", "/api/channels/create"),
            json=data,
            auth=True,
            lower=True,
            remove_none=False,
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    async def featured(self) -> list[Channel]:
        """トレンドのチャンネルを取得します

        Endpoint: `/api/channels/featured`

        Returns
        -------
        list[Channel]
            取得したチャンネルのリスト
        """

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/featured"), auth=True, lower=True
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    async def get_all_followed(
        self, since_id: str | None = None, until_id: str | None = None, limit: int = 5
    ) -> AsyncGenerator[Channel, None]:
        """フォロー中のすべてのチャンネルを取得します

        Endpoint: `/api/channels/followed`

        Parameters
        ----------
        since_id : str | None
            指定したチャンネルIDよりも後のチャンネルを取得します, default=None
        until_id : str | None
            指定したチャンネルIDよりも前のチャンネルを取得します, default=None
        limit : int, optional
            一度に取得するチャンネルの数, default=5

        Returns
        -------
        AsyncGenerator[Channel, None]
            取得したフォロー中のチャンネル
        """

        body = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IChannel](
            self._session, Route("POST", "/api/channels/followed"), json=body, auth=True
        )

        while pagination.is_final is False:
            for raw_channel in await pagination.next():
                yield Channel(raw_channel=raw_channel, client=self._client)

    async def owned(
        self, since_id: str | None = None, until_id: str | None = None, limit: int = 5
    ) -> list[Channel]:
        """自分が所有しているチャンネル一覧を取得します

        Endpoint: `/api/channels/owned`

        Parameters
        ----------
        since_id : str, optional
            指定したチャンネルIDよりも後のチャンネルを取得します, default=None
        until_id : str, optional
            指定したチャンネルIDよりも前のチャンネルを取得します, default=None
        limit : int, optional
            一度に取得するチャンネルの数, default=5

        Returns
        -------
        list[Channel]
            取得した自分が所有しているチャンネルのリスト
        """
        data = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/owned"), auth=True, json=data
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    async def get_all_owned(
        self, since_id: str | None = None, until_id: str | None = None, limit: int = 5
    ) -> AsyncGenerator[Channel, None]:
        """自分が所有しているすべてのチャンネルを取得します

        Endpoint: `/api/channels/owned`

        Parameters
        ----------
        since_id : str, optional
            指定したチャンネルIDよりも後のチャンネルを取得します, default=None
        until_id : str, optional
            指定したチャンネルIDよりも前のチャンネルを取得します, default=None
        limit : int, optional
            一度に取得するチャンネルの数, default=5

        Returns
        -------
        AsyncGenerator[Channel, None]
            取得した自分が所有しているチャンネル
        """

        body = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IChannel](
            self._session, Route("POST", "/api/channels/owned"), json=body, auth=True
        )

        while pagination.is_final is False:
            for raw_channel in await pagination.next():
                yield Channel(raw_channel=raw_channel, client=self._client)

    async def show(self, channel_id: str) -> Channel:
        """指定したIDのチャンネルを取得します

        Endpoint: `/api/channels/show`

        Parameters
        ----------
        channel_id : str
            対象のチャンネルID

        Returns
        -------
        Channel
            取得したチャンネル
        """
        raw_channel: IChannel = await self._session.request(
            Route("POST", "/api/channels/show"), auth=True, json={"channelId": channel_id}
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    async def my_favorites(self) -> list[Channel]:
        """自分がお気に入りにしているチャンネルを取得します

        Endpoint: `/api/channels/myFavorites`

        Returns
        -------
        list[Channel]
            取得したチャンネルのリスト
        """
        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/my-favorites"), auth=True, lower=True
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    async def search(
        self,
        query: str,
        type: Literal["nameAndDescription", "nameOnly"] = "nameAndDescription",
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 5,
    ) -> list[Channel]:
        """チャンネルを検索します

        Endpoint: `/api/channels/search`

        Parameters
        ----------
        query : str
            検索するキーワード
        type : Literal["nameAndDescription","nameOnly"]
            検索に用いる形式, default="nameAndDescription"
        since_id : str | None
            指定したIDのチャンネルより後のチャンネルを取得します, default=None
        until_id : str, optional
            指定したIDのチャンネルより前のチャンネルを取得します, default=None
        limit : int, optional
            一度に取得するチャンネルの数, default=5

        Returns
        -------
        list[Channel]
            見つかったチャンネルのリスト
        """

        data = {
            "query": query,
            "type": type,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
        }

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/search"), auth=True, json=data
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]
