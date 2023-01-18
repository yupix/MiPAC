from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.poll import PollActions

if TYPE_CHECKING:
    from mipac.http import HTTPClient
    from mipac.manager.client import ClientManager


class PollManager(AbstractManager):
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

    @property
    def action(self) -> PollActions:
        return PollActions(
            note_id=self.__note_id,
            session=self.__session,
            client=self.__client,
        )
