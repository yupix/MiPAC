from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.channel import Channel
from mipac.models.lite.channel import ChannelLite
from mipac.types.channel import IChannel
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

    async def favorite(self, channel_id: str | None = None):
        """
        Favorite a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        bool
            True if success else False
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise Exception()

        res: bool = await self._session.request(
            Route("POST", "/api/channels/favorite"), auth=True, json={"channelId": channel_id}
        )

        return res

    async def unfavorite(self, channel_id: str | None = None):
        """
        Unfavorite a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        bool
            True if success else False
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise Exception()

        res: bool = await self._session.request(
            Route("POST", "/api/channels/unfavorite"), auth=True, json={"channelId": channel_id}
        )

        return res

    async def follow(self, channel_id: str | None = None) -> bool:
        """
        Follow a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        bool
            True if success else False
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise ParameterError("required channel_id")

        res: bool = await self._session.request(
            Route("POST", "/api/channels/follow"), auth=True, json={"channelId": channel_id}
        )

        return res

    async def unfollow(self, channel_id: str | None = None) -> bool:
        """
        Unfollow a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        bool
            True if success else False
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise ParameterError("required channel_id")

        res: bool = await self._session.request(
            Route("POST", "/api/channels/unfollow"), auth=True, json={"channelId": channel_id}
        )

        return res

    async def update(
        self,
        name: str | None = None,
        description: str | None = None,
        banner_id: str | None = None,
        is_archived: bool | None = None,
        pinned_note_ids: list[str] | None = None,
        color: str | None = None,
        *,
        channel_id: str | None = None,
    ) -> Channel:
        """
        Update a channel.

        Parameters
        ----------
        name : str, optional, by default None
            Channel name
        description : str, optional, by default None
            Channel description
        banner_id : str, optional, by default None
            Channel banner id
        is_archived : bool, optional, by default None
            Channel is archived
        pinned_note_ids : list[str], optional, by default None
            Channel pinned note ids
        color : str, optional, by default None
            Channel color
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        Channel
            Channel
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise ParameterError("required channel_id")

        body = {
            "channelId": channel_id,
            "name": name,
            "description": description,
            "bannerId": banner_id,
            "isArchived": is_archived,
            "pinnedNoteIds": pinned_note_ids,
            "color": color,
        }
        res: IChannel = await self._session.request(
            Route("POST", "/api/channels/update"), auth=True, json=body
        )

        return Channel(res, client=self._client)

    async def archive(self, channel_id: str | None = None) -> Channel:
        """
        Archive a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        Channel
            Channel
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise ParameterError("required channel_id")

        res = await self.update(channel_id=channel_id, is_archived=True)

        return res

    async def unarchive(self, channel_id: str | None = None) -> Channel:
        """
        Unarchive a channel.

        Parameters
        ----------
        channel_id : str, optional, by default None
            Channel id

        Returns
        -------
        Channel
            Channel
        """
        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise ParameterError("required channel_id")

        res = await self.update(channel_id=channel_id, is_archived=False)

        return res


class ChannelActions(ClientChannelActions):
    def __init__(
        self, channel_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        super().__init__(channel_id=channel_id, session=session, client=client)

    async def create(
        self,
        name: str,
        description: str | None = None,
        banner_id: str | None = None,
        color: str = "#000",
    ) -> ChannelLite:
        """
        Create a channel.

        Parameters
        ----------
        name : str
            Channel name.
        description : str, optional, by default None
            Channel description
        banner_id : str, optional, by default None
            Channel banner id
        color : str, optional, by default '#000'
            Channel color

        Returns
        -------
        Channel
            ChannelLite
        """
        body = {"name": name, "description": description, "bannerId": banner_id, "color": color}
        res: IChannel = await self._session.request(
            Route("POST", "/api/channels/create"), auth=True, json=body
        )

        return ChannelLite(res, client=self._client)

    async def get_featured(self) -> list[Channel]:
        """
        Get featured channels.

        Returns
        -------
        list[Channel]
            Channel
        """
        res: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/featured"), auth=True
        )
        return [Channel(i, client=self._client) for i in res]

    async def get_followed(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[Channel, None]:
        """
        Get followed channels.

        Parameters
        ----------
        since_id : str, optional, by default None
            Since id
        until_id : str, optional, by default None
            Until id
        limit : int, optional, by default 10
            Limit
        get_all : bool, optional, by default False
            Get all channels flag

        Yields
        -------
        AsyncGenerator[Channel, None]
            Channel
        """
        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {"sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IChannel](
            self._session, Route("POST", "/api/channels/followed"), auth=True, json=body
        )

        while True:
            raw_channels = await pagination.next()
            for raw_channel in raw_channels:
                yield Channel(raw_channel, client=self._client)

            if get_all is False or pagination.is_final:
                break

    async def get_owned(
        self, since_id: str | None = None, until_id: str | None = None, *, get_all: bool = False
    ) -> AsyncGenerator[Channel, None]:
        """
        Get owned channels.

        Parameters
        ----------
        since_id : str, optional, by default None
            Since id
        until_id : str, optional, by default None
            Until id
        get_all : bool, optional, by default False
            Get all channels flag

        Yields
        ------
        AsyncGenerator[Channel, None]
            Channel
        """
        body = {"sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IChannel](
            self._session, Route("POST", "/api/channels/owned"), auth=True, json=body
        )

        while True:
            raw_channels = await pagination.next()
            for raw_channel in raw_channels:
                yield Channel(raw_channel, client=self._client)

            if get_all is False or pagination.is_final:
                break

    async def get(self, channel_id: str) -> Channel:
        """
        Get a channel.

        Parameters
        ----------
        channel_id : str
            Channel id

        Returns
        -------
        Channel
            Channel
        """
        res: IChannel = await self._session.request(
            Route("POST", "/api/channels/show"), auth=True, json={"channelId": channel_id}
        )
        return Channel(res, client=self._client)

    async def get_my_favorite(self) -> list[Channel]:
        """
        Get my favorite channels.

        Returns
        -------
        list[Channel]
            Channel
        """
        res: list[IChannel] = await self._session.request(
            Route("POST", "/api/channels/my-favorites"), auth=True
        )
        return [Channel(i, client=self._client) for i in res]

    async def search(
        self,
        query: str,
        type: Literal["nameAndDescription", "nameOnly"] = "nameAndDescription",
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 5,
        get_all: bool = False,
    ) -> AsyncGenerator[Channel, None]:
        """
        Search channels.

        Parameters
        ----------
        query : str
            Search query
        type : Literal['nameAndDescription', 'nameOnly'], optional, by default 'nameAndDescription'
            Search type
        since_id : str, optional, by default None
            Since id
        until_id : str, optional, by default None
            Until id
        limit : int, optional, by default 5
            Limit
        get_all : bool, optional, by default False
            Get all channels flag

        Yields
        ------
        AsyncGenerator[Channel, None]
            Channel
        """
        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {
            "query": query,
            "type": type,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
        }

        pagination = Pagination[IChannel](
            self._session, Route("POST", "/api/channels/search"), auth=True, json=body
        )

        while True:
            raw_channels = await pagination.next()
            for raw_channel in raw_channels:
                yield Channel(raw_channel, client=self._client)

            if get_all is False or pagination.is_final:
                break
