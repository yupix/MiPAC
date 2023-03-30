import asyncio
import uuid
from urllib.parse import urlencode

import aiohttp

from mipac.utils.format import remove_dict_empty


class AuthClient:
    """
    Tokenの取得を手助けするクラス
    """

    def __init__(
        self,
        instance_uri: str,
        name: str,
        description: str,
        permissions: list[str] | None = None,
        *,
        icon: str | None = None,
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
        icon: str | None, default=None
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
        self.__icon: str | None = icon
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
            {'name': self.__name, 'description': self.__description, 'icon': self.__icon}
        )
        if self.__use_miauth:
            field['permissions'] = self.__permissions
            query = urlencode(field)
            self.__session_token = uuid.uuid4()
            return f'{self.__instance_uri}/miauth/{self.__session_token}?{query}'
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
                json={'appSecret': self.__secret, 'token': self.__session_token},
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
