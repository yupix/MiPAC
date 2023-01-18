from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.models.lite.instance import LiteInstance
from mipac.types.emoji import ICustomEmojiLite
from mipac.types.user import ILiteUser
from mipac.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.user import UserManager


class LiteUser:
    __slots__ = ('__user', '__client')

    def __init__(self, user: ILiteUser, *, client: ClientManager) -> None:
        self.__user: ILiteUser = user
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__user['id']

    @property
    def username(self) -> str:
        return self.__user['username']

    @property
    def host(self) -> str | None:
        return self.__user['host'] if 'host' in self.__user else None

    @property
    @deprecated
    def name(self) -> str:
        return self.__user['name']

    @property
    def nickname(self) -> str:
        return self.__user['name']

    @property
    def online_status(
        self,
    ) -> Literal['online', 'active', 'offline', 'unknown']:
        return self.__user['online_status']

    @property
    def avatar_url(self) -> str:
        return self.__user['avatar_url']

    @property
    def avatar_blurhash(self) -> str:
        return self.__user['avatar_blurhash']

    @property
    def avatar_color(self) -> str | None:
        """
        Returns the average color of the avatar.
        Note: Since avatar_color is deprecated in v13,
        only None is returned for v13 instances.

        Returns
        -------
        str | None
            average color of the avatar
        """

        return self.__user.get('avatar_color')

    @property
    def emojis(self) -> list[ICustomEmojiLite]:  # TODO: ちゃんとモデルにする
        """
        List of emoji included in nicknames, etc
        Note: emojis have been abolished since misskey v13

        Returns
        -------
        list[ICustomEmojiLite]
            List of emoji included in nicknames, etc
        """

        return self.__user.get('emojis', [])

    @property
    def instance(self) -> LiteInstance | None:
        return (
            LiteInstance(self.__user['instance'])
            if 'instance' in self.__user
            else None
        )

    @property
    def api(self) -> UserManager:
        return self.__client._create_user_instance(self)
