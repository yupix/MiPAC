from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.config import config
from mipac.errors.base import NotSupportVersion
from mipac.http import Route
from mipac.models.emoji import CustomEmoji
from mipac.models.note import NoteReaction
from mipac.types.meta import ILiteMeta
from mipac.types.note import INoteReaction
from mipac.util import remove_dict_empty

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class ReactionActions(AbstractAction):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager
    ):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def add(self, reaction: str, note_id: str | None = None) -> bool:
        """
        指定したnoteに指定したリアクションを付与します（内部用

        Parameters
        ----------
        reaction : str | None
            付与するリアクション名
        note_id : str | None
            付与対象のノートID

        Returns
        -------
        bool
            成功したならTrue,失敗ならFalse
        """
        note_id = note_id or self.__note_id

        data = remove_dict_empty({'noteId': note_id, 'reaction': reaction})
        route = Route('POST', '/api/notes/reactions/create')
        res: bool = await self.__session.request(
            route, json=data, auth=True, lower=True
        )
        return bool(res)

    async def remove(self, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        data = remove_dict_empty({'noteId': note_id})
        route = Route('POST', '/api/notes/reactions/delete')
        res: bool = await self.__session.request(
            route, json=data, auth=True, lower=True
        )
        return bool(res)

    async def get_reaction(
        self, reaction: str, note_id: str | None = None, *, limit: int = 11
    ) -> list[NoteReaction]:
        note_id = note_id or self.__note_id
        data = remove_dict_empty(
            {'noteId': note_id, 'limit': limit, 'type': reaction}
        )
        res: list[INoteReaction] = await self.__session.request(
            Route('POST', '/api/notes/reactions'),
            json=data,
            auth=True,
            lower=True,
        )
        return [NoteReaction(i, client=self.__client) for i in res]

    async def get_emoji_list(self) -> list[CustomEmoji]:
        if config.use_version >= 13:
            raise NotSupportVersion('Misskey v13以降では使用できません')

        data: ILiteMeta = await self.__session.request(
            Route('GET', '/api/meta'),
            json={'detail': False},
            auth=True,
            replace_list={'ToSUrl': 'tos_url', 'ToSTextUrl': 'tos_text_url'},
        )
        return [
            CustomEmoji(i, client=self.__client)
            for i in data.get('emojis', [])
        ]
