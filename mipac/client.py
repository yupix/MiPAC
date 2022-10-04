from typing import Optional

from mipac.config import Config
from mipac.http import HTTPClient
from mipac.manager.client import ClientActions


class Client:
    def __init__(
        self, url: str, token: str, *, config: Optional[Config] = None
    ):
        self.__url: str = url
        self.__token: str = token
        self.__config: Config = config or Config()
        self.http: HTTPClient = HTTPClient(url, token)

    @property
    def api(self):
        return ClientActions(self.http, self.__config)

    async def close_session(self):
        await self.http.close_session()
