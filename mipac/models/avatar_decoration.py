from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.types.avatar_decoration import IAvatarDecoration
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.admins.avatar_decorations import ClientAdminAvatarDecorationManager
    from mipac.client import ClientManager


class AvatarDecoration:
    def __init__(self, raw_avatar_decoration: IAvatarDecoration, *, client: ClientManager):
        self.__raw_avatar_decoration: IAvatarDecoration = raw_avatar_decoration
        self.__api: ClientAdminAvatarDecorationManager = (
            client.admin._create_client_admin_avatar_decoration_manager(
                avatar_decoration_id=self.id
            )
        )

    @property
    def id(self) -> str:
        return self.__raw_avatar_decoration["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__raw_avatar_decoration["created_at"])

    @property
    def updated_at(self) -> datetime | None:
        if self.__raw_avatar_decoration["updated_at"] is None:
            return None

        return str_to_datetime(self.__raw_avatar_decoration["updated_at"])

    @property
    def url(self) -> str:
        return self.__raw_avatar_decoration["url"]

    @property
    def category(self) -> str | None:
        return self.__raw_avatar_decoration["category"]

    @property
    def role_ids_that_can_be_used_this_decoration(self) -> list[str]:
        return self.__raw_avatar_decoration["role_ids_that_can_be_used_this_decoration"]

    @property
    def api(self) -> ClientAdminAvatarDecorationManager:
        return self.__api
