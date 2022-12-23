from __future__ import annotations

import sys
from typing import Any, Literal, TypeVar

import aiohttp

from mipac import __version__
from mipac.exception import APIError
from mipac.types.endpoints import ENDPOINTS
from mipac.types.user import IUserDetailed
from mipac.util import _from_json, remove_dict_empty, upper_to_lower


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
    def __init__(self, url: str, token: str) -> None:
        user_agent = (
            'Misskey Bot (https://github.com/yupix/MiPA {0})'
            + 'Python/{1[0]}.{1[1]} aiohttp/{2}'
        )
        self.user_agent = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self._session: aiohttp.ClientSession = MISSING
        self._url: str = url
        self._token: str = token

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def request(self, route: Route, **kwargs) -> R:
        headers: dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        is_lower = kwargs.pop('lower') if kwargs.get('lower') else False

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['json'] = kwargs.pop('json')

        if kwargs.get('auth') and kwargs.pop('auth'):
            key = (
                'json' if 'json' in kwargs or 'data' not in kwargs else 'data'
            )
            if not kwargs.get(key):
                kwargs[key] = {}
            kwargs[key]['i'] = self._token

        replace_list = kwargs.pop('replace_list', {})

        for i in ('json', 'data'):
            if kwargs.get(i):
                kwargs[i] = remove_dict_empty(kwargs[i])
        async with self._session.request(
            route.method, self._url + route.path, **kwargs
        ) as res:
            data = await json_or_text(res)
            if is_lower:
                if isinstance(data, list):
                    data = [
                        upper_to_lower(i, replace_list=replace_list)
                        for i in data
                    ]
                if isinstance(data, dict):
                    data = upper_to_lower(data)
            if 300 > res.status >= 200:
                return data  # type: ignore
            if 511 > res.status >= 300:
                raise APIError(data, res.status)
            raise APIError('HTTP ERROR')

    async def close_session(self) -> None:
        await self._session.close()

    async def login(self) -> IUserDetailed:
        self._session = aiohttp.ClientSession(
            ws_response_class=MisskeyClientWebSocketResponse
        )
        data: IUserDetailed = await self.request(
            Route('POST', '/api/i'), auth=True
        )
        return data
