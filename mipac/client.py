from mipac.config import Config, config
from mipac.http import HTTPClient
from mipac.manager.client import ClientManager


class Client:
    def __init__(self, url: str, token: str) -> None:
        self.__url: str = url
        self.__token: str = token
        self.config: Config = config
        self.http: HTTPClient = HTTPClient(url, token)

    @property
    def api(self) -> ClientManager:
        return ClientManager(self.http, self.config)

    async def close_session(self) -> None:
        await self.http.close_session()
