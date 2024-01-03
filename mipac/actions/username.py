from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.username import UsernameAvailable
from mipac.types.username import IUsernameAvailable

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class UsernameActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def available(self, username: str) -> UsernameAvailable:
        data = {"username": username}
        res: IUsernameAvailable = await self.__session.request(
            Route("POST", "/api/username/available"), json=data, auth=True
        )
        return UsernameAvailable(res)
