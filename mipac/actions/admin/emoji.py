from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotExistRequiredData
from mipac.http import Route
from mipac.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientActions


class AdminEmojiActions(AbstractAction):
    def __init__(
        self,
        emoji_id: None | str = None,
        *,
        session: HTTPClient,
        client: ClientActions
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

        if self.__client._config.is_official:
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
            if self.__client._config.is_official
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
