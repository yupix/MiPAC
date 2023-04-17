from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.channel import Channel
from mipac.types.channel import IChannel

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
        if self._client._config.use_version < 13:
            raise Exception()

        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise Exception()

        res: bool = await self._session.request(
            Route('POST', '/api/channels/favorite'), auth=True, json={'channelId': channel_id}
        )

        return res

    async def unfavorite(self, channel_id: str | None = None):

        if self._client._config.use_version < 13:
            raise Exception()

        channel_id = self._channel_id or channel_id
        if channel_id is None:
            raise Exception()

        res: bool = await self._session.request(
            Route('POST', '/api/channels/unfavorite'), auth=True, json={'channelId': channel_id}
        )

        return res


class ChannelActions(ClientChannelActions):
    def __init__(
        self, channel_id: str | None = None, *, session: HTTPClient, client: ClientManager
    ):
        super().__init__(channel_id=channel_id, session=session, client=client)

    async def get_my_favorite(self) -> list[Channel]:
        """お気に入りに登録したチャンネルの一覧を取得します。

        Returns
        -------
        Channel
            チャンネル
        """
        if self._client._config.use_version < 13:
            raise Exception()

        res: list[IChannel] = await self._session.request(
            Route('POST', '/api/channels/my-favorites'), auth=True
        )
        return [Channel(i, client=self._client) for i in res]
