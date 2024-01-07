from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.note import ClientNoteActions, NoteActions
from mipac.http import HTTPClient
from mipac.manager.favorite import ClientFavoriteManager, FavoriteManager
from mipac.manager.poll import ClientPollManager, PollManager
from mipac.manager.reaction import ClientReactionManager, ReactionManager

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientNoteManager(AbstractManager):
    def __init__(self, note_id: str, *, session: HTTPClient, client: ClientManager):
        self.__note_id = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.reaction: ClientReactionManager = ClientReactionManager(
            note_id=note_id, session=session, client=client
        )
        self.favorite = ClientFavoriteManager(note_id=note_id, session=session, client=client)
        self.poll: ClientPollManager = ClientPollManager(
            note_id=note_id, session=session, client=client
        )

    @property
    def action(self) -> ClientNoteActions:
        return ClientNoteActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )


class NoteManager(AbstractManager):
    """User behavior for notes"""

    def __init__(self, note_id: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__note_id: str | None = note_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client
        self.reaction: ReactionManager = ReactionManager(session=session, client=client)
        self.favorite = FavoriteManager(note_id=note_id, session=session, client=client)
        self.poll: PollManager = PollManager(note_id=note_id, session=session, client=client)
        self.__action: NoteActions = NoteActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )  # property側で生成するとcacheが効かなくなる

    @property
    def action(self) -> NoteActions:
        return self.__action
