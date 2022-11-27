"""
MiPAを使用する上でちょっとした際に便利なツール一覧
"""
from __future__ import annotations

import asyncio
import functools
import json
import re
import uuid
import warnings
from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import urlencode

import aiohttp
from _operator import itemgetter

try:
    import orjson  # type: ignore
except ModuleNotFoundError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True

__all__ = (
    'deprecated',
    'MiTime',
    'get_cache_key',
    'key_builder',
    'check_multi_arg',
    'remove_list_empty',
    'remove_dict_empty',
    'upper_to_lower',
    'str_lower',
    'bool_to_string',
    '_from_json',
)


if HAS_ORJSON:
    _from_json = orjson.loads  # type: ignore
else:
    _from_json = json.loads

DEFAULT_CACHE: dict[str, list[dict[str, Any]]] = {}


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(
            'Call to deprecated function {}.'.format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


class MiTime:
    def __init__(self, start: timedelta, end: datetime):
        self.start = start
        self.end = end


class AuthClient:
    """
    Tokenの取得を手助けするクラス
    """

    def __init__(
        self,
        instance_uri: str,
        name: str,
        description: str,
        permissions: Optional[list[str]] = None,
        *,
        icon: Optional[str] = None,
        use_miauth: bool = False,
    ):
        """
        Parameters
        ----------
        instance_uri : str
            アプリケーションを作成したいインスタンスのURL
        name : str
            アプリケーションの名前
        description : str
            アプリケーションの説明
        permissions : Optional[list[str]], default=None
            アプリケーションが要求する権限
        icon: Optional[str], default=None
            アプリケーションのアイコン画像URL
        use_miauth: bool, default=False
            MiAuthを使用するか
        """
        if permissions is None:
            permissions = ['read:account']
        self.__client_session = aiohttp.ClientSession()
        self.__instance_uri: str = instance_uri
        self.__name: str = name
        self.__description: str = description
        self.__permissions: list[str] = permissions
        self.__icon: Optional[str] = icon
        self.__use_miauth: bool = use_miauth
        self.__session_token: uuid.UUID
        self.__secret: str

    async def get_auth_url(self) -> str:
        """
        認証に使用するURLを取得します

        Returns
        -------
        str
            認証に使用するURL
        """
        field = remove_dict_empty(
            {
                'name': self.__name,
                'description': self.__description,
                'icon': self.__icon,
            }
        )
        if self.__use_miauth:
            field['permissions'] = self.__permissions
            query = urlencode(field)
            self.__session_token = uuid.uuid4()
            return (
                f'{self.__instance_uri}/miauth/{self.__session_token}?{query}'
            )
        else:
            field['permission'] = self.__permissions
            async with self.__client_session.post(
                f'{self.__instance_uri}/api/app/create', json=field
            ) as res:
                data = await res.json()
                self.__secret = data['secret']
            async with self.__client_session.post(
                f'{self.__instance_uri}/api/auth/session/generate',
                json={'appSecret': self.__secret},
            ) as res:
                data = await res.json()
                self.__session_token = data['token']
                return data['url']

    async def wait_miauth(self) -> str:
        url = f'{self.__instance_uri}/api/miauth/{self.__session_token}/check'
        while True:
            async with self.__client_session.post(url) as res:
                data = await res.json()
                if data.get('ok') is True:
                    return data
            await asyncio.sleep(1)

    async def wait_oldauth(self) -> None:
        while True:
            async with self.__client_session.post(
                f'{self.__instance_uri}/api/auth/session/userkey',
                json={
                    'appSecret': self.__secret,
                    'token': self.__session_token,
                },
            ) as res:
                data = await res.json()
                if data.get('error', {}).get('code') != 'PENDING_SESSION':
                    break
            await asyncio.sleep(1)

    async def check_auth(self) -> str:
        """
        認証が完了するまで待機し、完了した場合はTokenを返します

        Returns
        -------
        str
            Token
        """
        if self.__use_miauth:
            data = await self.wait_miauth()
        else:
            data = await self.wait_oldauth()
        await self.__client_session.close()
        return data['token'] if self.__use_miauth else data['accessToken']


def dynamic_args(decorator):
    def wrapper(*args, **kwargs):
        if len(args) != 0 and callable(args[0]):
            func = args[0]
            return functools.wraps(func)(decorator(func))
        else:

            def _wrapper(func):
                return functools.wraps(func)(decorator(func, *args, **kwargs))

            return _wrapper

    return wrapper


def set_cache(group: str, key: str, value: Any):
    if len(DEFAULT_CACHE.get(group, [])) > 50:
        del DEFAULT_CACHE[group][-1]

    if DEFAULT_CACHE.get(group) is None:
        DEFAULT_CACHE[group] = []
    DEFAULT_CACHE[group].append({key: value})


def get_cache(group: str, key: str):
    if DEFAULT_CACHE.get(group):
        return list(map(itemgetter(key), DEFAULT_CACHE[group]))[0]
    return None


@dynamic_args
def cache(func, group: str = 'default', override: bool = False):
    async def decorator(self, *args, **kwargs):
        ordered_kwargs = sorted(kwargs.items())
        key = '.{0}' + str(args) + str(ordered_kwargs)
        hit_item = get_cache(group, key)
        if hit_item and override is False:
            return hit_item
        res = await func(self, *args, **kwargs)
        set_cache(group, key, res)
        return res

    return decorator


def get_cache_key(func):
    async def decorator(self, *args, **kwargs):
        ordered_kwargs = sorted(kwargs.items())
        key = (
            (func.__module__ or '')
            + '.{0}'
            + f'{self}'
            + str(args)
            + str(ordered_kwargs)
        )
        return await func(self, *args, **kwargs, cache_key=key)

    return decorator


def key_builder(func, cls, *args, **kwargs):
    ordered_kwargs = sorted(kwargs.items())
    key = (
        (func.__module__ or '')
        + f'.{func.__name__}'
        + f'{cls}'
        + str(args)
        + str(ordered_kwargs)
    )
    return key


def check_multi_arg(*args: Any) -> bool:
    """
    複数の値を受け取り値が存在するかをboolで返します

    Parameters
    ----------
    args : list
        確認したい変数のリスト

    Returns
    -------
    bool
        存在する場合はTrue, 存在しない場合はFalse
    """
    return bool([i for i in args if i])


def remove_list_empty(data: list[Any]) -> list[Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    dict[str, Any]
        空のkeyがなくなったdict
    """
    return [k for k in data if k]


def remove_dict_empty(data: dict[str, Any]) -> dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    _data: dict
        空のkeyがなくなったdict
    """
    _data = {}
    _data = {k: v for k, v in data.items() if v is not None}
    _data = {k: v for k, v in data.items() if v}
    return _data


def upper_to_lower(
    data: dict[str, Any],
    field: Optional[dict[str, Any]] = None,
    nest: bool = True,
    replace_list: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        小文字にしたいkeyがあるdict
    field: dict, default=None
        謎
    nest: bool, default=True
        ネストされたdictのkeyも小文字にするか否か
    replace_list: dict, default=None
        dictのkey名を特定の物に置き換える

    Returns
    -------
    field : dict
        小文字になった, key名が変更されたdict
    """
    if data is None:
        return {}
    if replace_list is None:
        replace_list = {}

    if field is None:
        field = {}
    for attr in data:
        pattern = re.compile('[A-Z]')
        large = [i.group().lower() for i in pattern.finditer(attr)]
        result = [None] * (len(large + pattern.split(attr)))
        result[::2] = pattern.split(attr)
        result[1::2] = ['_' + i.lower() for i in large]
        default_key = ''.join(result)
        if replace_list.get(attr):
            default_key = default_key.replace(attr, replace_list.get(attr))
        field[default_key] = data[attr]
        if isinstance(field[default_key], dict) and nest:
            field[default_key] = upper_to_lower(field[default_key])
    return field


def str_lower(text: str):
    pattern = re.compile('[A-Z]')
    large = [i.group().lower() for i in pattern.finditer(text)]
    result = [None] * (len(large + pattern.split(text)))
    result[::2] = pattern.split(text)
    result[1::2] = ['_' + i.lower() for i in large]
    return ''.join(result)


def bool_to_string(boolean: bool) -> str:
    """
    boolを小文字にして文字列として返します

    Parameters
    ----------
    boolean : bool
        変更したいbool値
    Returns
    -------
    true or false: str
        小文字になったbool文字列
    """
    return 'true' if boolean else 'false'
