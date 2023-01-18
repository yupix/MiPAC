from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.note import Note
from mipac.types.note import INote

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class PollActions(AbstractAction):
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

    async def vote(self, choice: int, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        if note_id is None:
            raise ParameterError('note_id is required')

        data = {'noteId': note_id, 'choice': choice}
        res: bool = await self.__session.request(
            Route('POST', '/api/notes/polls/vote'), auth=True, json=data
        )
        return res

    async def recommendation(
        self, limit: int = 100, offset: int = 0, all: bool = True
    ):

        if limit > 100:
            raise ParameterError('limit must be less than 100')

        if all:
            limit = 100

        async def request(body) -> list[Note]:
            res: list[INote] = await self.__session.request(
                Route('POST', '/api/notes/polls/recommendation'),
                lower=True,
                auth=True,
                json=body,
            )
            return [Note(note, client=self.__client) for note in res]

        data = {'limit': limit, 'offset': offset}
        first_res: list[Note] = await request(data)
        for note in first_res:
            yield note
        offset = limit
        count = 1
        if all and len(first_res) == limit:
            data['offset'] = limit * count
            while True:
                res = await request(data)
                if len(res) <= limit:
                    for note in res:
                        yield note
                if len(res) == 0 or len(res) < limit:
                    break
                data['offset'] = limit * count
                count = count + 1
