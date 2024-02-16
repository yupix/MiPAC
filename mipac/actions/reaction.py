from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.emoji import CustomEmoji
from mipac.models.note import NoteReaction
from mipac.types.meta import IPartialMeta
from mipac.types.note import INoteReaction
from mipac.utils.cache import cache
from mipac.utils.format import remove_dict_empty

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedReactionActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager) -> None:
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def add(self, reaction: str, *, note_id: str) -> bool:
        """Add reaction to note

        Endpoint: `/api/notes/reactions/create`

        Parameters
        ----------
        reaction : str
            reaction
        note_id : str, optional
            note id, by default None

        Returns
        -------
        bool
            success or not
        """
        data = remove_dict_empty({"noteId": note_id, "reaction": reaction})
        route = Route("POST", "/api/notes/reactions/create")
        res: bool = await self._session.request(route, json=data, auth=True, lower=True)
        return bool(res)

    async def remove(self, *, note_id: str) -> bool:
        """Remove reaction from note

        Endpoint: `/api/notes/reactions/delete`

        Parameters
        ----------
        note_id : str, optional
            note id, by default None

        Returns
        -------
        bool
            success or not
        """
        data = remove_dict_empty({"noteId": note_id})
        route = Route("POST", "/api/notes/reactions/delete")
        res: bool = await self._session.request(route, json=data, auth=True, lower=True)
        return bool(res)

    @cache(group="get_note_reaction")
    async def get_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str,
    ) -> list[NoteReaction]:
        data = remove_dict_empty(
            {
                "noteId": note_id,
                "limit": limit,
                "type": type,
                "sinceId": since_id,
                "untilId": until_id,
            }
        )
        res: list[INoteReaction] = await self._session.request(
            Route("POST", "/api/notes/reactions"),
            json=data,
            auth=True,
            lower=True,
        )
        return [NoteReaction(i, client=self._client) for i in res]

    @cache(group="get_note_reaction", override=True)
    async def fetch_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str,
    ) -> list[NoteReaction]:
        return await self.get_reactions(
            type=type, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )


class ClientReactionActions(SharedReactionActions):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager) -> None:
        super().__init__(session=session, client=client)
        self.__note_id: str = note_id

    @override
    async def add(self, reaction: str, *, note_id: str | None = None) -> bool:
        """Add reaction to note

        Endpoint: `/api/notes/reactions/create`

        Parameters
        ----------
        reaction : str
            reaction
        note_id : str, optional
            note id, by default None

        Returns
        -------
        bool
            success or not
        """

        note_id = note_id or self.__note_id

        return await super().add(reaction=reaction, note_id=note_id)

    @override
    async def remove(self, *, note_id: str | None = None) -> bool:
        """Remove reaction from note

        Endpoint: `/api/notes/reactions/delete`

        Parameters
        ----------
        note_id : str, optional
            note id, by default None

        Returns
        -------
        bool
            success or not
        """
        note_id = note_id or self.__note_id

        return await super().remove(note_id=note_id)

    @override
    async def get_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str | None = None,
    ) -> list[NoteReaction]:
        note_id = note_id or self.__note_id

        return await super().get_reactions(
            type=type, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )

    @override
    async def fetch_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str | None = None,
    ) -> list[NoteReaction]:
        note_id = note_id or self.__note_id

        return await super().fetch_reactions(
            type=type, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )


class ReactionActions(SharedReactionActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def get_emoji_list(
        self,
    ) -> list[CustomEmoji]:  # TODO: metaからemojisは削除されてるので別の方法に切り替える
        data: IPartialMeta = await self._session.request(
            Route("GET", "/api/meta"),
            json={"detail": False},
            auth=True,
            replace_list={"ToSUrl": "tos_url", "ToSTextUrl": "tos_text_url"},
        )
        return [CustomEmoji(i, client=self._client) for i in data.get("emojis", [])]
