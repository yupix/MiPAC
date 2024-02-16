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


class ClientReactionActions(AbstractAction):
    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

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

        data = remove_dict_empty({"noteId": note_id, "reaction": reaction})
        route = Route("POST", "/api/notes/reactions/create")
        res: bool = await self.__session.request(route, json=data, auth=True, lower=True)
        return bool(res)

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

        data = remove_dict_empty({"noteId": note_id})
        route = Route("POST", "/api/notes/reactions/delete")
        res: bool = await self.__session.request(route, json=data, auth=True, lower=True)
        return bool(res)

    @cache(group="get_note_reaction")
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

        if note_id is None:
            raise ValueError("note_id is required.")

        data = remove_dict_empty(
            {
                "noteId": note_id,
                "limit": limit,
                "type": type,
                "sinceId": since_id,
                "untilId": until_id,
            }
        )
        res: list[INoteReaction] = await self.__session.request(
            Route("POST", "/api/notes/reactions"),
            json=data,
            auth=True,
            lower=True,
        )
        return [NoteReaction(i, client=self.__client) for i in res]

    @cache(group="get_note_reaction", override=True)
    async def fetch_reactions(
        self,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        note_id: str | None = None,
    ) -> list[NoteReaction]:
        return await self.get_reactions(
            type=type, note_id=note_id, limit=limit, since_id=since_id, until_id=until_id
        )


class ReactionActions(ClientReactionActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    @override
    async def add(self, note_id: str, reaction: str):
        return await super().add(reaction=reaction, note_id=note_id)

    @override
    async def remove(self, note_id: str):
        return await super().remove(note_id=note_id)

    @override
    async def get_reactions(
        self,
        note_id: str,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ):
        return await super().get_reactions(
            type=type, limit=limit, since_id=since_id, until_id=until_id, note_id=note_id
        )

    @override
    async def fetch_reactions(
        self,
        note_id: str,
        type: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
    ):
        return await super().fetch_reactions(
            type=type, limit=limit, since_id=since_id, until_id=until_id, note_id=note_id
        )

    async def get_emoji_list(
        self,
    ) -> list[CustomEmoji]:  # TODO: metaからemojisは削除されてるので別の方法に切り替える
        data: IPartialMeta = await self.__session.request(
            Route("GET", "/api/meta"),
            json={"detail": False},
            auth=True,
            replace_list={"ToSUrl": "tos_url", "ToSTextUrl": "tos_text_url"},
        )
        return [CustomEmoji(i, client=self.__client) for i in data.get("emojis", [])]
