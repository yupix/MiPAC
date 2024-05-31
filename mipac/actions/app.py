from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.app import App
from mipac.types.app import IApp

if TYPE_CHECKING:
    from mipac.client import ClientManager


class AppActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def create(
        self, name: str, description: str, permission: list[str], callback_url: str | None = None
    ) -> App:
        """Create a new app

        Parameters
        ----------
        name : str
            The name of the app
        description : str
            The description of the app
        permission : list[str]
            The permissions the app has
        callback_url : str, optional
            The callback url of the app, by default None

        Returns
        -------
        App
            The created app
        """

        body = {
            "name": name,
            "description": description,
            "permission": permission,
            "callbackUrl": callback_url,
        }

        raw_app: IApp = await self.__session.request(Route("POST", "/api/app/create"), json=body)
        return App(raw_app)

    async def show(self, app_id: str) -> App:
        """Show an app

        Parameters
        ----------
        app_id : str
            The id of the app

        Returns
        -------
        App
            The app
        """

        raw_app: IApp = await self.__session.request(
            Route("POST", "/api/app/show"), json={"appId": app_id}
        )
        return App(raw_app)
