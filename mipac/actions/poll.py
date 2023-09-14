from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.types.note import INote
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class PollActions(AbstractAction):
    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def vote(self, choice: int, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        if note_id is None:
            raise ParameterError("note_id is required")

        data = {"noteId": note_id, "choice": choice}
        res: bool = await self.__session.request(
            Route("POST", "/api/notes/polls/vote"), auth=True, json=data
        )
        return res

    async def recommendation(self, limit: int = 100, offset: int = 0, get_all: bool = True):
        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        data = {"limit": limit, "offset": offset}

        pagination = Pagination[INote](
            self.__session,
            Route("POST", "/api/notes/polls/recommendation"),
            json=data,
            pagination_type="count",
        )

        while True:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self.__client)
            if get_all is False or pagination.is_final:
                break
