from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from mipac.actions.hashtag import HashtagActions

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class HashtagManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> HashtagActions:
        return HashtagActions(session=self.__session, client=self.__client)
