from typing import Literal

from mipac.models.lite.instance import LiteInstance
from mipac.types.emoji import ICustomEmojiLite
from mipac.types.user import IUserLite


class LiteUser:
    __slots__ = ('__user',)

    def __init__(self, user: IUserLite) -> None:
        self.__user: IUserLite = user

    @property
    def id(self) -> str:
        return self.__user['id']

    @property
    def username(self) -> str:
        return self.__user['username']

    @property
    def host(self) -> str | None:
        return self.__user['host']

    @property
    def name(self) -> str:
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
    def emojis(self) -> list[ICustomEmojiLite]:  # TODO: ちゃんとモデルにする
        return self.__user['emojis']

    @property
    def instance(self) -> LiteInstance:
        return LiteInstance(self.__user['instance'])
