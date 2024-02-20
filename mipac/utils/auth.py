import asyncio
import uuid
from typing import Any, Literal, NotRequired, TypedDict
from urllib.parse import urlencode, urlparse, urlunparse

import aiohttp

from mipac.types.permission import Permissions
from mipac.types.user import IUserDetailed
from mipac.utils.format import remove_dict_empty, upper_to_lower


class IMiAuthPayload(TypedDict):
    ok: bool
    token: NotRequired[str]
    user: NotRequired[IUserDetailed]


class MiAuth:
    """Misskey v12以降のインスタンスで使用可能な認証方式です"""

    def __init__(self, host: str, protocol: Literal["http", "https"]) -> None:
        self.host: str = host
        self.protocol: Literal["http", "https"] = protocol
        self.session: str

        self.set_session()

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}"

    def set_session(self) -> None:
        self.session = uuid.uuid4().hex

    async def gen_session(
        self,
        name: str | None = None,
        icon: str | None = None,
        callback: str | None = None,
        permission: list[Permissions] | None = None,
    ):
        # sessionは使いまわししてはいけないのでこのタイミングで新しいsessionを生成する
        self.set_session()

        query = remove_dict_empty(
            {
                "name": name,
                "icon": icon,
                "callback": callback,
                "permission": ",".join(permission) if permission else None,
            }
        )

        url = urlparse(f"{self.url}/miauth/{self.session}")
        return urlunparse(
            (url.scheme, url.netloc, url.path, url.params, urlencode(query), url.fragment)
        )

    async def check_session(self) -> Any:
        async with aiohttp.ClientSession() as session:
            res = await session.post(
                f"{self.url}/api/miauth/{self.session}/check",
                json={},
                headers={"Content-Type": "application/json"},
            )

            if res.status != 200:
                raise Exception(f"MiAuth Check failed, Status code: {res.status}")

            data = await res.json()

            if data is None:
                raise Exception("MiAuth Check failed, Response is None")
            return upper_to_lower(data)

    async def wait_complete(self):
        while True:
            is_complete: IMiAuthPayload = await self.check_session()
            if is_complete["ok"] is True:
                break
            await asyncio.sleep(1)

        return is_complete
