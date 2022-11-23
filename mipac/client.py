from typing import Optional

from mipac.config import Config
from mipac.http import HTTPClient
from mipac.manager.client import ClientActions


class Client:
    def __init__(
        self, url: str, token: str, *, config: Optional[Config] = None
    ) -> None:
        self.__url: str = url
        self.__token: str = token
        self.__config: Config = config or Config()
        self.http: HTTPClient = HTTPClient(url, token)

    @property
    def api(self) -> ClientActions:
        return ClientActions(self.http, self.__config)

    async def close_session(self) -> None:
        await self.http.close_session()
