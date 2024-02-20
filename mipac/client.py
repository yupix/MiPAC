from typing import Self

from mipac.config import Config, config
from mipac.http import HTTPClient
from mipac.manager.client import ClientManager
from mipac.utils.log import LOGING_LEVEL_TYPE, setup_logging


class Client:
    def __init__(
        self,
        url: str,
        token: str | None = None,
        *,
        log_level: LOGING_LEVEL_TYPE | None = "INFO",
    ) -> None:
        if log_level is not None:
            setup_logging(level=log_level)
        self.config: Config = config
        self.http: HTTPClient = HTTPClient(url, token)

    async def __aenter__(self) -> Self:
        await self.http.login()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close_session()

    @property
    def api(self) -> ClientManager:
        return ClientManager(self.http, self.config)

    async def close_session(self) -> None:
        await self.http.close_session()
