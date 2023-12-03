from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator
from typing_extensions import override

from mipac.abstract.action import AbstractAction
from mipac.file import MiFile
from mipac.http import HTTPClient, Route
from mipac.models.channel import Channel
from mipac.models.drive import File
from mipac.models.poll import MiPoll
from mipac.types.channel import IChannel
from mipac.types.note import INote, INoteVisibility
from mipac.types.reaction import IReactionAcceptance
from mipac.utils.format import remove_dict_missing
from mipac.utils.util import MISSING, credentials_required
from mipac.models.note import Note
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientChannelActions(AbstractAction):
    def __init__(
        self, channel_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        self._channel_id: str | None = channel_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @credentials_required
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

    @credentials_required
    async def follow(self, *, channel_id: str | None = None) -> bool:
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
        channel_id = channel_id or self._channel_id
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/follow"), json=data, auth=True, lower=True
        )
        return res

    @credentials_required
    async def unfollow(self, *, channel_id: str | None = None) -> bool:
        """Unfollow a channel

        Endpoint: `/api/channels/unfollow`

        Parameters
        ----------
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        bool
            Whether the channel is unfollowed
        """
        channel_id = channel_id or self._channel_id
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/unfollow"), json=data, auth=True, lower=True
        )
        return res

    async def timeline(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
        *,
        channel_id: str | None = None,
    ) -> list[Note]:
        """Get the timeline of a channel

        Endpoint: `/api/channels/timeline`

        Parameters
        ----------
        limit : int, optional
            Limit, by default 10
        since_id : str, optional
            Since ID, by default None
        until_id : str, optional
            Until ID, by default None
        since_date : int, optional
            Since date, by default None
        until_date : int, optional
            Until date, by default None

        Returns
        -------
        list[Note]
            List of notes
        """
        channel_id = channel_id or self._channel_id
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
        channel_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Get all notes in the timeline of a channel

        Parameters
        ----------
        since_id : str, optional
            Since ID, by default None
        until_id : str, optional
            Until ID, by default None
        since_date : int, optional
            Since date, by default None
        until_date : int, optional
            Until date, by default None

        Returns
        -------
        AsyncGenerator[Note, None]
            Async generator of notes
        """
        channel_id = channel_id or self._channel_id
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
        channel_id: str | None = None,
    ) -> Channel:
        """Update a channel

        Endpoint: `/api/channels/update`

        Parameters
        ----------
        name : str, optional
            Name of the channel, by default MISSING
        description : str, optional
            Description of the channel, by default MISSING
        banner_id : str, optional
            Banner ID of the channel, by default MISSING
        is_archived : bool, optional
            Whether the channel is archived, by default MISSING
        pinned_note_ids : list[str], optional
            Pinned note IDs, by default MISSING
        color : str, optional
            Color of the channel, by default MISSING
        is_sensitive : bool, optional
            Whether the channel is sensitive, by default MISSING
        allow_renote_to_external : bool, optional
            Whether the channel allows renote to external, by default MISSING
        channel_id : str, optional
            ID of the channel, by default None
        """
        channel_id = channel_id or self._channel_id
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
            Route("POST", "/api/channels/update"),
            json=data,
            auth=True,
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    @credentials_required
    async def favorite(self, *, channel_id: str | None = None) -> bool:
        """Favorite a channel

        Endpoint: `/api/channels/favorite`

        Parameters
        ----------
        channel_id : str, optional
            ID of the channel, by default None

        Returns
        -------
        bool
            Whether the channel is favorited
        """
        channel_id = channel_id or self._channel_id
        data = {"channelId": channel_id}

        res: bool = await self._session.request(
            Route("POST", "/api/channels/favorite"), json=data, auth=True, lower=True
        )
        return res


class ChannelActions(ClientChannelActions):
    def __init__(
        self, channel_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        super().__init__(channel_id=channel_id, session=session, client=client)

    @credentials_required
    @override
    async def send(
        self,
        channel_id: str,
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

    @credentials_required
    async def create(
        self,
        name: str,
        color: str,
        description: str | None = None,
        banner_id: str | None = None,
        is_sensitive: bool | None = None,
        allow_renote_to_external: bool | None = None,
    ) -> Channel:
        """Create a channel

        Endpoint: `/api/channels/create`

        Parameters
        ----------
        name : str
            Name of the channel
        color : str
            Color of the channel
        description : str, optional
            Description of the channel, by default None
        banner_id : str, optional
            Banner ID of the channel, by default None
        is_sensitive : bool, optional
            Whether the channel is sensitive, by default None
        allow_renote_to_external : bool, optional
            Whether the channel allows renote to external, by default None

        Returns
        -------
        Channel
            Created channel
        """
        data = {
            "name": name,
            "color": color,
            "description": description,
            "banner_id": banner_id,
            "is_sensitive": is_sensitive,
            "allow_renote_to_external": allow_renote_to_external,
        }
        raw_channel: IChannel = await self._session.request(
            Route("POST", "/api/channels/create"),
            json=data,
            auth=True,
            lower=True,
            remove_none=False,
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    async def featured(self) -> list[Channel]:
        """Get featured channels

        Endpoint: `/api/channels/featured`

        Returns
        -------
        list[Channel]
            List of featured channels
        """

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/featured"), auth=True, lower=True
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    @credentials_required
    @override
    async def follow(self, channel_id: str) -> bool:
        """Follow a channel

        Endpoint: `/api/channels/follow`

        Parameters
        ----------
        channel_id : str
            ID of the channel

        Returns
        -------
        bool
            Whether the channel is followed
        """
        return await super().follow(channel_id=channel_id)

    @credentials_required
    async def followed(
        self, since_id: str | None = None, until_id: str | None = None, limit: int = 5
    ) -> list[Channel]:
        """Get followed channels

        Endpoint: `/api/channels/followed`

        Parameters
        ----------
        since_id : str, optional
            Since ID, by default None
        until_id : str, optional
            Until ID, by default None
        limit : int, optional
            Limit, by default 5

        Returns
        -------
        list[Channel]
            List of followed channels
        """
        data = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/followed"), auth=True, json=data
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    @credentials_required
    async def owned(
        self, since_id: str | None = None, until_id: str | None = None, limit: int = 5
    ) -> list[Channel]:
        """Get owned channels

        Endpoint: `/api/channels/owned`

        Parameters
        ----------
        since_id : str, optional
            Since ID, by default None
        until_id : str, optional
            Until ID, by default None
        limit : int, optional
            Limit, by default 5

        Returns
        -------
        list[Channel]
            List of owned channels
        """
        data = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        raw_channels: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/owned"), auth=True, json=data
        )
        return [
            Channel(raw_channel=raw_channel, client=self._client) for raw_channel in raw_channels
        ]

    async def show(self, channel_id: str) -> Channel:
        """Show a channel

        Endpoint: `/api/channels/show`

        Parameters
        ----------
        channel_id : str
            ID of the channel

        Returns
        -------
        Channel
            Channel
        """
        raw_channel: IChannel = await self._session.request(
            Route("POST", "/api/channels/show"), auth=True, json={"channelId": channel_id}
        )
        return Channel(raw_channel=raw_channel, client=self._client)

    @credentials_required
    @override
    async def unfollow(self, channel_id: str) -> bool:
        """Unfollow a channel

        Endpoint: `/api/channels/unfollow`

        Parameters
        ----------
        channel_id : str
            ID of the channel

        Returns
        -------
        bool
            Whether the channel is unfollowed
        """
        return await super().unfollow(channel_id=channel_id)

    @override
    async def get_all_timeline(
        self,
        channel_id: str,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: int | None = None,
        until_date: int | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Get all notes in the timeline of a channel

        Parameters
        ----------
        channel_id : str
            ID of the channel
        since_id : str, optional
            Since ID, by default None
        until_id : str, optional
            Until ID, by default None
        since_date : int, optional
            Since date, by default None
        until_date : int, optional
            Until date, by default None

        Returns
        -------
        AsyncGenerator[Note, None]
            Async generator of notes
        """
        async for i in super().get_all_timeline(
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            channel_id=channel_id,
        ):
            yield i

    @credentials_required
    @override
    async def update(
        self,
        channel_id: str,
        name: str | None = MISSING,
        description: str | None = MISSING,
        banner_id: str | None = MISSING,
        is_archived: bool | None = MISSING,
        pinned_note_ids: list[str] | None = MISSING,
        color: str | None = MISSING,
        is_sensitive: bool | None = MISSING,
        allow_renote_to_external: bool | None = MISSING,
    ) -> Channel:
        """Update a channel

        Endpoint: `/api/channels/update`

        Parameters
        ----------
        channel_id : str
            ID of the channel
        name : str, optional
            Name of the channel, by default MISSING
        description : str, optional
            Description of the channel, by default MISSING
        banner_id : str, optional
            Banner ID of the channel, by default MISSING
        is_archived : bool, optional
            Whether the channel is archived, by default MISSING
        pinned_note_ids : list[str], optional
            Pinned note IDs, by default MISSING
        color : str, optional
            Color of the channel, by default MISSING
        is_sensitive : bool, optional
            Whether the channel is sensitive, by default MISSING
        allow_renote_to_external : bool, optional
            Whether the channel allows renote to external, by default MISSING

        Returns
        -------
        Channel
            Updated channel
        """

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

    @credentials_required
    @override
    async def favorite(self, channel_id: str) -> bool:
        """Favorite a channel

        Endpoint: `/api/channels/favorite`

        Parameters
        ----------
        channel_id : str
            ID of the channel

        Returns
        -------
        bool
            Whether the channel is favorited
        """
        return await super().favorite(channel_id=channel_id)
