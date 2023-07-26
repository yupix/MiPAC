from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.actions.clip import ClipActions
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientClipManager(AbstractManager):
    def __init__(
        self, clip_id: str | None = None, *, session: HTTPClient, client: ClientManager,
    ):
        self.__clip_id = clip_id
        self.__session = session
        self.__client = client

    @property
    def action(self) -> ClipActions:
        return ClipActions(clip_id=self.__clip_id, session=self.__session, client=self.__client,)


class ClipManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    @property
    def action(self) -> ClipActions:
        return ClipActions(session=self.__session, client=self.__client)

    def _get_client_clip_instance(self, *, clip_id: str | None = None) -> ClientClipManager:
        return ClientClipManager(clip_id=clip_id, session=self.__session, client=self.__client)
