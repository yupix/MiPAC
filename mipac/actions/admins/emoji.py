from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotExistRequiredData, ParameterError
from mipac.http import Route
from mipac.models.emoji import CustomEmoji
from mipac.types.emoji import ICustomEmoji
from mipac.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class AdminEmojiActions(AbstractAction):
    def __init__(
        self,
        emoji_id: None | str = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__emoji_id = emoji_id
        self.__session = session
        self.__client = client

    async def add(
        self,
        file_id: str | None = None,
        *,
        name: str | None = None,
        url: str | None = None,
        category: str | None = None,
        aliases: list[str] | None = None
    ) -> bool:
        """絵文字を追加します

        Parameters
        ----------
        file_id : str | None, optional
            追加する絵文字のファイルId, by default None
        name : str | None, optional
            絵文字名, by default None
        url : str | None, optional
            絵文字があるUrl, by default None
        category : str | None, optional
            絵文字のカテゴリー, by default None
        aliases : list[str] | None, optional
            絵文字のエイリアス, by default None

        Returns
        -------
        bool
            成功したかどうか

        Raises
        ------
        NotExistRequiredData
            必要なデータが不足している
        """

        if self.__client._config.use_version >= 12:
            data = {'fileId': file_id}
        else:
            data = {
                'name': name,
                'url': url,
                'category': category,
                'aliases': aliases,
            }

        if not check_multi_arg(file_id, url):
            raise NotExistRequiredData('required a file_id or url')
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/emoji/add'),
                json=data,
                lower=True,
                auth=True,
            )
        )

    async def gets(
        self,
        query: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        all: bool = True
    ) -> AsyncIterator[CustomEmoji]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if all:
            limit = 100

        async def request(body) -> list[CustomEmoji]:
            res: list[ICustomEmoji] = await self.__session.request(
                Route('POST', '/api/admin/emoji/list'), auth=True, json=body,
            )
            return [CustomEmoji(emoji, client=self.__client) for emoji in res]

        body = {
            'query': query,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }
        first_req = await request(body)

        for emoji in first_req:
            yield emoji
        if all and len(first_req) == 100:
            body['untilId'] = first_req[-1].id
            count = 0
            while True:
                count = count + 1
                res = await request(body)
                if len(res) <= 100:
                    for emoji in res:
                        yield emoji
                if len(res) < 100:
                    print(res[-1].id)
                    break

    async def gets_remote(
        self,
        query: str | None = None,
        host: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        all: bool = True
    ) -> AsyncIterator[CustomEmoji]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if all:
            limit = 100

        async def request(body) -> list[CustomEmoji]:
            res: list[ICustomEmoji] = await self.__session.request(
                Route('POST', '/api/admin/emoji/list-remote'),
                auth=True,
                json=body,
            )
            return [CustomEmoji(emoji, client=self.__client) for emoji in res]

        body = {
            'query': query,
            'host': host,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }
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

    async def remove(self, emoji_id: str | None = None) -> bool:
        """指定したIdの絵文字を削除します

        Parameters
        ----------
        emoji_id : str | None, optional
            削除する絵文字のId, by default None

        Returns
        -------
        bool
            成功したかどうか

        Raises
        ------
        NotExistRequiredData
            Idが不足している
        """

        emoji_id = emoji_id or self.__emoji_id

        if emoji_id is None:
            raise NotExistRequiredData('idが不足しています')

        endpoint = (
            '/api/admin/emoji/delete'
            if self.__client._config.use_version >= 12
            else '/api/admin/emoji/remove'
        )

        return bool(
            await self.__session.request(
                Route('POST', endpoint),
                auth=True,
                json={'id': emoji_id},
                lower=True,
            )
        )
