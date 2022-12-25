from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class PollActions(AbstractAction):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def vote(self, choice: int, note_id: str | None = None) -> bool:
        note_id = note_id or self.__note_id

        if note_id is None:
            raise ParameterError('note_id is required')

        data = {'noteId': note_id, 'choice': choice}
        res: bool = await self.__session.request(
            Route('POST', '/api/notes/polls/vote'), auth=True, json=data
        )
        return res
