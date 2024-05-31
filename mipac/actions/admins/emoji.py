from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.common import ID
from mipac.models.emoji import EmojiDetailed
from mipac.types.common import IID
from mipac.types.emoji import IEmojiDetailed
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedAdminEmojiAction(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def copy(self, *, emoji_id: str):
        """Copy an emoji

        Parameters
        ----------
        emoji_id : str
            The id of the emoji
        """
        raw_id: IID = await self.__session.request(
            Route("POST", "/api/admin/emoji/copy"), json={"emojiId": emoji_id}
        )

        return ID(raw_id=raw_id)

    async def delete(self, *, emoji_id: str) -> bool:
        """Delete an emoji

        Parameters
        ----------
        id : str
            The id of the emoji

        Returns
        -------
        bool
            Whether the operation was successful
        """
        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/delete"), json={"id": emoji_id}
        )

        return res

    async def update(
        self,
        name: str = MISSING,
        file_id: str = MISSING,
        category: str | None = MISSING,
        aliases: list[str] | None = MISSING,
        is_sensitive: bool = MISSING,
        local_only: bool = MISSING,
        role_ids_that_can_be_used_this_emoji_as_reaction: list[str] = MISSING,
        *,
        emoji_id: str,
    ) -> bool:
        """Update an emoji

        Parameters
        ----------
        name : str
            The name of the emoji
        file_id : str
            The id of the file
        category : str, optional
            The category of the emoji, by default None
        aliases : list[str], optional
            The aliases of the emoji, by default None
        is_sensitive : bool
            Whether the emoji is sensitive
        local_only : bool
            Whether the emoji is local only
        role_ids_that_can_be_used_this_emoji_as_reaction : list[str]
            The role ids that can be used this emoji as reaction
        emoji_id : str
            The id of the emoji

        Returns
        -------
        bool
            Whether the operation was successful
        """

        body = remove_dict_missing(
            {
                "id": emoji_id,
                "name": name,
                "fileId": file_id,
                "category": category,
                "aliases": aliases,
                "isSensitive": is_sensitive,
                "localOnly": local_only,
                "roleIdsThatCanBeUsedThisEmojiAsReaction": role_ids_that_can_be_used_this_emoji_as_reaction,
            }
        )

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/update"), json=body
        )
        return res


class ClientAdminEmojiAction(SharedAdminEmojiAction):
    def __init__(self, *, emoji_id: str, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__emoji_id: str = emoji_id

    @override
    async def copy(self, *, emoji_id: str | None = None) -> ID:
        emoji_id = emoji_id or self.__emoji_id

        return await super().copy(emoji_id=emoji_id)

    @override
    async def delete(self, *, emoji_id: str | None = None) -> bool:
        emoji_id = emoji_id or self.__emoji_id

        return await super().delete(emoji_id=emoji_id)

    @override
    async def update(
        self,
        name: str = MISSING,
        file_id: str = MISSING,
        category: str | None = MISSING,
        aliases: list[str] | None = MISSING,
        is_sensitive: bool = MISSING,
        local_only: bool = MISSING,
        role_ids_that_can_be_used_this_emoji_as_reaction: list[str] = MISSING,
        *,
        emoji_id: str | None = None,
    ) -> bool:
        emoji_id = emoji_id or self.__emoji_id

        return await super().update(
            name=name,
            file_id=file_id,
            category=category,
            aliases=aliases,
            is_sensitive=is_sensitive,
            local_only=local_only,
            role_ids_that_can_be_used_this_emoji_as_reaction=role_ids_that_can_be_used_this_emoji_as_reaction,
            emoji_id=emoji_id,
        )


class AdminEmojiAction(SharedAdminEmojiAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def add_aliases_bulk(self, ids: list[str], aliases: list[str]) -> bool:
        """Add aliases to emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis
        aliases : list[str]
            The aliases to add

        Returns
        -------
        bool
            Whether the operation was successful
        """
        body = {"ids": ids, "aliases": aliases}

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/add-aliases-bulk"), json=body
        )

        return res

    async def add(
        self,
        name: str,
        file_id: str,
        category: str | None = None,
        aliases: list[str] | None = None,
        license: str | None = None,
        is_sensitive: bool = MISSING,
        local_only: bool = MISSING,
    ) -> EmojiDetailed:
        """Add a new emoji

        Parameters
        ----------
        name : str
            The name of the emoji
        file_id : str
            The id of the file
        category : str, optional
            The category of the emoji, by default None
        aliases : list[str], optional
            The aliases of the emoji, by default None
        license : str, optional
            The license of the emoji, by default None
        is_sensitive : bool
            Whether the emoji is sensitive
        local_only : bool
            Whether the emoji is local only

        Returns
        -------
        EmojiDetailed
            The added emoji
        """

        body = remove_dict_missing(
            {
                "name": name,
                "fileId": file_id,
                "category": category,
                "aliases": aliases,
                "license": license,
                "isSensitive": is_sensitive,
                "localOnly": local_only,
            }
        )

        raw_emoji: IEmojiDetailed = await self.__session.request(
            Route("POST", "/api/admin/emoji/add"), json=body
        )

        return EmojiDetailed(raw_emoji, client=self.__client)

    async def delete_bulk(self, ids: list[str]) -> bool:
        """Delete emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis

        Returns
        -------
        bool
            Whether the operation was successful
        """
        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/delete-bulk"), json={"ids": ids}
        )

        return res

    async def get_list_remote(
        self,
        query: str | None = None,
        host: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[EmojiDetailed]:
        """List remote emojis

        Parameters
        ----------
        query : str, optional
            The query to search for, by default None
        host : str, optional
            The host of the emoji, by default None
        limit : int, optional
            The limit of the emojis to get, by default 10
        since_id : str, optional
            The id to get emojis since, by default None
        until_id : str, optional
            The id to get emojis until, by default None

        Returns
        -------
        list[EmojiDetailed]
            The emojis
        """
        body = remove_dict_missing(
            {
                "query": query,
                "host": host,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
            }
        )

        raw_emojis: list[IEmojiDetailed] = await self.__session.request(
            Route("POST", "/api/admin/emoji/list-remote"), json=body
        )

        return [EmojiDetailed(raw_emoji, client=self.__client) for raw_emoji in raw_emojis]

    async def get_all_list_remote(
        self,
        query: str | None = None,
        host: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> AsyncGenerator[EmojiDetailed, None]:
        """List remote emojis

        Parameters
        ----------
        query : str, optional
            The query to search for, by default None
        host : str, optional
            The host of the emoji, by default None
        limit : int, optional
            The limit of the emojis to get, by default 10
        since_id : str, optional
            The id to get emojis since, by default None
        until_id : str, optional
            The id to get emojis until, by default None

        Yields
        ------
        AsyncGenerator[EmojiDetailed, None]
            The emojis
        """
        body = remove_dict_missing(
            {
                "query": query,
                "host": host,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
            }
        )

        pagination = Pagination[IEmojiDetailed](
            self.__session, Route("POST", "/api/admin/emoji/list-remote"), body
        )

        while pagination.is_final is False:
            for raw_emoji in await pagination.next():
                yield EmojiDetailed(raw_emoji, client=self.__client)

    async def get_list(
        self,
        query: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> list[EmojiDetailed]:
        """List emojis

        Parameters
        ----------
        query : str, optional
            The query to search for, by default None
        limit : int, optional
            The limit of the emojis to get, by default 10
        since_id : str, optional
            The id to get emojis since, by default None
        until_id : str, optional
            The id to get emojis until, by default None

        Returns
        -------
        list[EmojiDetailed]
            The emojis
        """
        body = remove_dict_missing(
            {"query": query, "limit": limit, "sinceId": since_id, "untilId": until_id}
        )

        raw_emojis: list[IEmojiDetailed] = await self.__session.request(
            Route("POST", "/api/admin/emoji/list"), json=body
        )

        return [EmojiDetailed(raw_emoji, client=self.__client) for raw_emoji in raw_emojis]

    async def get_all_list(
        self,
        query: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ) -> AsyncGenerator[EmojiDetailed, None]:
        """List all emojis

        Parameters
        ----------
        query : str, optional
            The query to search for, by default None
        limit : int, optional
            The limit of the emojis to get, by default 10
        since_id : str, optional
            The id to get emojis since, by default None
        until_id : str, optional
            The id to get emojis until, by default None

        Yields
        ------
        AsyncGenerator[EmojiDetailed, None]
            The emojis
        """

        body = remove_dict_missing(
            {"query": query, "limit": limit, "sinceId": since_id, "untilId": until_id}
        )

        pagination = Pagination[IEmojiDetailed](
            self.__session, Route("POST", "/api/admin/emoji/list"), body
        )

        while pagination.is_final is False:
            for raw_emoji in await pagination.next():
                yield EmojiDetailed(raw_emoji, client=self.__client)

    async def remove_aliases_bulk(self, ids: list[str], aliases: list[str]) -> bool:
        """Remove aliases from emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis
        aliases : list[str]
            The aliases to remove

        Returns
        -------
        bool
            Whether the operation was successful
        """
        body = {"ids": ids, "aliases": aliases}

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/remove-aliases-bulk"), json=body
        )

        return res

    async def set_aliases_bulk(self, ids: list[str], aliases: list[str]) -> bool:
        """Set aliases to emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis
        aliases : list[str]
            The aliases to set

        Returns
        -------
        bool
            Whether the operation was successful
        """
        body = {"ids": ids, "aliases": aliases}

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/set-aliases-bulk"), json=body
        )

        return res

    async def set_category_bulk(self, ids: list[str], category: str) -> bool:
        """Set category to emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis
        category : str
            The category to set

        Returns
        -------
        bool
            Whether the operation was successful
        """
        body = {"ids": ids, "category": category}

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/set-category-bulk"), json=body
        )

        return res

    async def set_license_bulk(self, ids: list[str], license: str) -> bool:
        """Set license to emojis in bulk

        Parameters
        ----------
        ids : list[str]
            The ids of the emojis
        license : str
            The license to set

        Returns
        -------
        bool
            Whether the operation was successful
        """
        body = {"ids": ids, "license": license}

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/emoji/set-license-bulk"), json=body
        )

        return res
