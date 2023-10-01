from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.models.lite.instance import LiteInstance
from mipac.types.emoji import ICustomEmojiLite
from mipac.types.user import IBadgeRole, ILiteUser

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.user import UserManager

T = TypeVar("T", bound=IBadgeRole)
LUT = TypeVar("LUT", bound=ILiteUser)


class BadgeRole(AbstractModel, Generic[T]):
    def __init__(self, data: T, *, client: ClientManager) -> None:
        self._data: T = data
        self._client = client

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def icon_url(self) -> str | None:
        return self._data["icon_url"]

    @property
    def display_order(self) -> int:
        return self._data["display_order"]


class LiteUser(AbstractModel, Generic[LUT]):
    __slots__ = ("_user", "__client")

    def __init__(self, user: LUT, *, client: ClientManager) -> None:
        self._user: LUT = user
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self._user["id"]

    @property
    def username(self) -> str:
        return self._user["username"]

    @property
    def host(self) -> str | None:
        host = self._user.get("host")
        return host if host else None

    @property
    def nickname(self) -> str:
        return self._user["name"]

    @property
    def online_status(
        self,
    ) -> Literal["online", "active", "offline", "unknown"]:
        return self._user["online_status"]

    @property
    def badge_roles(self) -> list[BadgeRole]:
        return [
            BadgeRole(data, client=self.__client) for data in self._user.get("badge_roles", [])
        ]

    @property
    def avatar_url(self) -> str:
        return self._user["avatar_url"]

    @property
    def avatar_blurhash(self) -> str:
        return self._user["avatar_blurhash"]

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

        return self._user.get("avatar_color")

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

        return self._user.get("emojis", [])

    @property
    def instance(self) -> LiteInstance | None:
        instance = self._user.get("instance")
        return LiteInstance(instance) if instance else None

    @property
    def api(self) -> UserManager:
        return self.__client._create_user_instance(self)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, LiteUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
