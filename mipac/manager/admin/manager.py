from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient, Route
from mipac.manager.ad import AdminAdvertisingManager
from mipac.manager.admin.emoji import AdminEmojiManager
from mipac.manager.admin.moderator import AdminModeratorManager
from mipac.manager.admin.user import AdminUserManager

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminManager(AbstractManager):
    def __init__(self, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.emoji = AdminEmojiManager(session=session, client=client)
        self.user = AdminUserManager(session=session, client=client)
        self.ad = AdminAdvertisingManager(session=session, client=client)
        self.moderator = AdminModeratorManager(session=session, client=client)

    async def get_invite(self) -> bool:
        return bool(
            await self.__session.request(Route('POST', '/api/admin/invite'))
        )
