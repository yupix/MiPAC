from __future__ import annotations

import json
import logging
import re
import sys
from typing import Any, Literal

import aiohttp

from mipac import __version__
from mipac.config import config
from mipac.errors.base import APIError
from mipac.types.endpoints import ENDPOINTS
from mipac.types.user import IMeDetailedSchema
from mipac.utils.format import remove_dict_empty, upper_to_lower
from mipac.utils.util import COLORS, _from_json, deprecated

_log = logging.getLogger(__name__)


class MisskeyClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = 4000, message: bytes = b"") -> bool:
        return await super().close(code=code, message=message)


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding="utf-8")
    try:
        if "application/json" in response.headers["Content-Type"]:
            return _from_json(text)
    except KeyError:
        pass


class Route:
    """MisskeyのAPIを使用するためのルートとメソッドを定義するクラス

    Parameters
    ----------
    method : Literal["GET", "POST"]
        メソッド
    path : ENDPOINTS
        ルートパス

    Attributes
    ----------
    path : str
        ルートパス
    method : str
        メソッド
    """

    def __init__(self, method: Literal["GET", "POST"], path: ENDPOINTS):
        self.path: str = path
        self.method: str = method


class HTTPClient:
    """MisskeyのAPIを使用するためのクライアントクラス

    Parameters
    ----------
    url : str
        MisskeyのURL
    token : str | None
        Misskeyのトークン
    """

    def __init__(self, url: str, token: str | None = None) -> None:
        user_agent = (
            "Misskey Bot (https://github.com/yupix/MiPA {0})" + "Python/{1[0]}.{1[1]} aiohttp/{2}"
        )
        self._url: str = url
        self._token: str | None = token
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self._session = aiohttp.ClientSession(ws_response_class=MisskeyClientWebSocketResponse)

        match_domain = re.search(r"https?:\/\/([^\/]+)", self._url)
        match_protocol = re.search(r"^(http|https)", self._url)
        if match_domain is None or match_protocol is None:
            raise Exception("Server URL cannot be retrieved or protocol (http / https) is missing")
        protocol = True if match_protocol.group(1) == "https" else False
        config.from_dict(
            host=match_domain.group(1),
            is_ssl=protocol,
        )

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close_session()

    @property
    def session(self) -> aiohttp.ClientSession:
        """現在のセッションを返します

        Returns
        -------
        aiohttp.ClientSession
            現在のセッション
        """
        return self._session

    async def request(
        self,
        route: Route,
        auth: bool = True,
        remove_none: bool = True,
        lower: bool = True,
        **kwargs,
    ) -> Any:
        headers: dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["json"] = kwargs.pop("json")

        if auth:
            key = "json" if "json" in kwargs or "data" not in kwargs else "data"
            if not kwargs.get(key):
                kwargs[key] = {}
            if self._token:
                kwargs[key]["i"] = self._token

        replace_list = kwargs.pop("replace_list", {})

        for i in ("json", "data"):
            if kwargs.get(i) and remove_none:
                kwargs[i] = remove_dict_empty(kwargs[i])
        async with self._session.request(route.method, self._url + route.path, **kwargs) as res:
            data = await json_or_text(res)
            if lower:
                if isinstance(data, list):
                    data = [upper_to_lower(i, replace_list=replace_list) for i in data]
                if isinstance(data, dict):
                    data = upper_to_lower(data)
            _log.debug(
                f"""{COLORS.green}
REQUEST:{COLORS.reset}
    {kwargs}
{COLORS.green}RESPONSE:{COLORS.reset}
    {json.dumps(data, ensure_ascii=False, indent=4) if data else data}
                """
            )
            if res.status == 204 and data is None:
                return True  # type: ignore
            if 300 > res.status >= 200:
                return data  # type: ignore
            if 511 > res.status >= 300:
                if isinstance(data, dict):
                    APIError(data, res.status).raise_error()
            APIError("HTTP ERROR", res.status).raise_error()

    async def close_session(self) -> None:
        """セッションを終了します"""
        await self._session.close()

    @deprecated
    async def login(self) -> IMeDetailedSchema | None:
        """現在指定されているTokenのユーザー情報を返します

        ..deprecated:: 0.6.4
            :class:`mipac.http.HTTPClient` をインスタンス化した際に自動的にセッションが作成されるようになったため非推奨になりました。現在のTokenのユーザー情報を取得する場合は :meth:`mipac.actions.user.get_me` を使用してください。

        Returns
        -------
        IMeDetailedSchema | None
            Tokenがある場合は自身の情報を返します。Tokenが無い場合はNoneを返します
        """
        if self._token:
            data: IMeDetailedSchema = await self.request(Route("POST", "/api/i"), auth=True)
            return data
