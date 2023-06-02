from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotExistRequiredData, ParameterError
from mipac.http import Route
from mipac.models.emoji import CustomEmoji
from mipac.types.emoji import ICustomEmoji
from mipac.utils.pagination import Pagination
from mipac.utils.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class AdminEmojiActions(AbstractAction):
    def __init__(self, emoji_id: None | str = None, *, session: HTTPClient, client: ClientManager):
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
                Route('POST', '/api/admin/emoji/add'), json=data, lower=True, auth=True,
            )
        )

    async def gets(
        self,
        query: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        get_all: bool = True
    ) -> AsyncGenerator[CustomEmoji, None]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if get_all:
            limit = 100

        body = {
            'query': query,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }

        pagination = Pagination[ICustomEmoji](
            self.__session, Route('POST', '/api/admin/emoji/list'), json=body
        )

        while True:
            res_custom_emojis = await pagination.next()
            for res_custom_emoji in res_custom_emojis:
                yield CustomEmoji(res_custom_emoji, client=self.__client)

            if get_all is False or pagination.is_final:
                break

    async def gets_remote(
        self,
        query: str | None = None,
        host: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        get_all: bool = True
    ) -> AsyncGenerator[CustomEmoji, None]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if get_all:
            limit = 100

        body = {
            'query': query,
            'host': host,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }

        pagination = Pagination[ICustomEmoji](
            self.__session, Route('POST', '/api/admin/emoji/list-remote'), json=body
        )

        while True:
            res_custom_emojis = await pagination.next()
            for res_custom_emoji in res_custom_emojis:
                yield CustomEmoji(res_custom_emoji, client=self.__client)

            if get_all is False or pagination.is_final:
                break

    async def set_license_bulk(self, ids: list[str], license: str | None = None) -> bool:
        body = {'ids': ids, 'license': license}
        res: bool = await self.__session.request(
            Route('POST', '/api/admin/emoji/set-license-bulk'),
            auth=True,
            json=body,
            remove_none=False,  # remove_noneをFalseにしないとlisenceが消せなくなる
        )
        return res

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
                Route('POST', endpoint), auth=True, json={'id': emoji_id}, lower=True,
            )
        )
