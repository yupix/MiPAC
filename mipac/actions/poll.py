from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.types.note import INote
from mipac.utils.pagination import Pagination
from mipac.utils.util import credentials_required

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientPollActions(AbstractAction):
    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self._note_id: str | None = note_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def vote(self, choice: int, *, note_id: str | None = None) -> bool:
        note_id = note_id or self._note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id, "choice": choice}
        res: bool = await self._session.request(
            Route("POST", "/api/notes/polls/vote"), auth=True, json=data
        )
        return res


class PollActions(ClientPollActions):
    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        super().__init__(note_id=note_id, session=session, client=client)

    @credentials_required
    async def recommendation(self, limit: int = 100, offset: int = 0):
        if limit > 100:
            raise ParameterError("limit must be less than 100")

        data = {"limit": limit, "offset": offset}

        res: list[INote] = await self._session.request(
            Route("POST", "/api/notes/polls/recommendation"), json=data, auth=True
        )
        return [Note(note, client=self._client) for note in res]

    @credentials_required
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
