from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedFavoriteActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(self, *, note_id: str) -> bool:
        data = {"noteId": note_id}
        return bool(
            await self._session.request(
                Route("POST", "/api/notes/favorites/create"),
                json=data,
                auth=True,
            )
        )

    @deprecated
    async def add(self, *, note_id: str) -> bool:
        return await self.create(note_id=note_id)

    async def delete(self, *, note_id: str) -> bool:
        data = {"noteId": note_id}
        return bool(
            await self._session.request(
                Route("POST", "/api/notes/favorites/delete"),
                json=data,
                auth=True,
            )
        )

    @deprecated
    async def remove(self, *, note_id: str) -> bool:
        return await self.delete(note_id=note_id)


class ClientFavoriteActions(SharedFavoriteActions):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__note_id: str = note_id

    @override
    async def create(self, *, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        return await super().create(note_id=note_id)

    @deprecated
    @override
    async def add(self, *, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        return await super().create(note_id=note_id)

    @override
    async def delete(self, *, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        return await super().delete(note_id=note_id)

    @deprecated
    @override
    async def remove(self, *, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        return await super().delete(note_id=note_id)


class FavoriteActions(SharedFavoriteActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
