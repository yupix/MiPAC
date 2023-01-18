from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import Route

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class FavoriteActions(AbstractAction):
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

    async def add(self, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/notes/favorites/create'),
                json=data,
                auth=True,
            )
        )

    async def remove(self, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/notes/favorites/delete'),
                json=data,
                auth=True,
            )
        )
