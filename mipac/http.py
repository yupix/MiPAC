from __future__ import annotations

import json
import logging
import re
import sys
from typing import Any, Literal, TypeVar

import aiohttp

from mipac import __version__
from mipac.config import config
from mipac.errors.base import APIError
from mipac.types.endpoints import ENDPOINTS
from mipac.types.meta import IMeta
from mipac.types.user import IUserDetailed
from mipac.utils.format import remove_dict_empty, upper_to_lower
from mipac.utils.util import COLORS, _from_json

_log = logging.getLogger(__name__)


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()
R = TypeVar('R')


class MisskeyClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = 4000, message: bytes = b'') -> bool:
        return await super().close(code=code, message=message)


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['Content-Type']:
            return _from_json(text)
    except KeyError:
        pass


class Route:
    def __init__(self, method: Literal['GET', 'POST'], path: ENDPOINTS):
        self.path: str = path
        self.method: str = method


class HTTPClient:
    def __init__(self, url: str, token: str | None = None) -> None:
        user_agent = (
            'Misskey Bot (https://github.com/yupix/MiPA {0})' + 'Python/{1[0]}.{1[1]} aiohttp/{2}'
        )
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self._session: aiohttp.ClientSession = MISSING
        self._url: str = url
        self._token: str | None = token

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def request(
        self,
        route: Route,
        auth: bool = False,
        remove_none: bool = True,
        lower: bool = True,
        **kwargs,
    ) -> R:
        headers: dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['json'] = kwargs.pop('json')

        if auth:
            key = 'json' if 'json' in kwargs or 'data' not in kwargs else 'data'
            if not kwargs.get(key):
                kwargs[key] = {}
            if self._token:
                kwargs[key]['i'] = self._token

        replace_list = kwargs.pop('replace_list', {})

        for i in ('json', 'data'):
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
                f'''{COLORS.green}
REQUEST:{COLORS.reset}
    {kwargs}
{COLORS.green}RESPONSE:{COLORS.reset}
    {json.dumps(data, ensure_ascii=False, indent=4) if data else data}
                '''
            )
            if res.status == 204 and data is None:
                return True  # type: ignore
            if 300 > res.status >= 200:
                return data  # type: ignore
            if 511 > res.status >= 300:
                if isinstance(data, dict):
                    APIError(data, res.status).raise_error()
            APIError('HTTP ERROR', res.status).raise_error()

    async def close_session(self) -> None:
        await self._session.close()

    async def login(self) -> IUserDetailed | None:
        match_domain = re.search(r'https?:\/\/([^\/]+)', self._url)
        match_protocol = re.search(r'^(http|https)', self._url)
        if match_domain is None or match_protocol is None:
            raise Exception()
        protocol = True if match_protocol.group(1) == 'https' else False
        config.from_dict(
            host=match_domain.group(1), is_ssl=protocol,
        )
        self._session = aiohttp.ClientSession(ws_response_class=MisskeyClientWebSocketResponse)
        if self._token:
            data: IUserDetailed = await self.request(Route('POST', '/api/i'), auth=True)
            if config.use_version_autodetect:
                meta: IMeta = await self.request(Route('POST', '/api/meta'), auth=True)
                use_version = int(meta['version'].split('.')[0])
                if isinstance(use_version, int) and use_version in (13, 12, 11):
                    config.use_version = use_version
            return data
