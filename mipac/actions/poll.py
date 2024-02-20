from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.types.note import INote
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedPollActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def vote(
        self,
        choice: int,
        *,
        note_id: str,
    ) -> bool:
        data = {"noteId": note_id, "choice": choice}
        res: bool = await self._session.request(
            Route("POST", "/api/notes/polls/vote"), auth=True, json=data
        )
        return res


class ClientPollActions(SharedPollActions):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self._note_id: str = note_id

    @override
    async def vote(self, choice: int, *, note_id: str | None = None) -> bool:
        note_id = note_id or self._note_id

        return await super().vote(choice=choice, note_id=note_id)


class PollActions(SharedPollActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def recommendation(self, limit: int = 100, offset: int = 0):
        if limit > 100:
            raise ValueError("limit must be less than 100")

        data = {"limit": limit, "offset": offset}

        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/polls/recommendation"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    async def get_all_recommendation(self, offset: int = 0):
        limit = 100

        data = {"limit": limit, "offset": offset}

        pagination = Pagination[INote](
            self._session,
            Route("POST", "/api/notes/polls/recommendation"),
            json=data,
            pagination_type="count",
            auth=True,
        )

        while True:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self._client)
            if pagination.is_final:
                break
