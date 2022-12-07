from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.abc.manager import AbstractManager
from mipac.actions.note import ClientNoteActions, NoteActions
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class ClientNoteManager(AbstractManager):
    def __init__(
        self,
        note_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.__note_id = note_id

    @property
    def action(self) -> ClientNoteActions:
        return ClientNoteActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )


class NoteManager(AbstractManager):
    """User behavior for notes"""

    def __init__(
        self,
        note_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.__note_id = note_id
        self.client = ClientNoteManager(session=session, client=client)

    def create_client_note_manager(self, note_id: str) -> ClientNoteManager:
        return ClientNoteManager(
            note_id=note_id, session=self.__session, client=self.__client
        )

    @property
    def action(self) -> NoteActions:
        return NoteActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )

    async def get(
        self,
        local: bool = True,
        reply: bool = False,
        renote: bool = True,
        with_files: bool = False,
        poll: bool = True,
        limit: int = 10,
        since_id: Optional[str] = None,
        until_id: Optional[str] = None,
    ):
        data = {
            'local': local,
            'reply': reply,
            'renote': renote,
            'withFiles': with_files,
            'poll': poll,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }
        await self.__session.request(
            Route('POST', '/api/notes'), json=data, auth=True, lower=True
        )
