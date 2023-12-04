from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.models.lite.instance import LiteInstance
from mipac.types.user import IBadgeRole, IPartialUser, IUserOnlineStatus, IAvatarDecoration
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.user import UserManager

T = TypeVar("T", bound=IBadgeRole)
PU = TypeVar("PU", bound=IPartialUser)


class BadgeRole(Generic[T]):
    def __init__(self, data: T, *, client: ClientManager) -> None:
        self._data: T = data
        self._client = client

    @property
    def name(self) -> str:
        """Returns the name of the badge role.

        Returns
        -------
        str
            The name of the badge role.
        """
        return self._data["name"]

    @property
    def icon_url(self) -> str | None:
        """Returns the icon url of the badge role.

        Returns
        -------
        str | None
            The icon url of the badge role.
        """
        return self._data["icon_url"]

    @property
    def display_order(self) -> int:
        """Returns the display order of the badge role.

        Returns
        -------
        int
            The display order of the badge role.
        """
        return self._data["display_order"]


class AvatarDecoration:
    def __init__(self, raw_avatar_decoration: IAvatarDecoration, *, client: ClientManager) -> None:
        self.__raw_avatar_decoration: IAvatarDecoration = raw_avatar_decoration
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """Returns the id of the avatar decoration.

        Returns
        -------
        str
            The id of the avatar decoration.
        """
        return self.__raw_avatar_decoration["id"]

    @property
    def angle(self) -> int:
        """Returns the angle of the avatar decoration.

        Returns
        -------
        int
            The angle of the avatar decoration.
        """
        return self.__raw_avatar_decoration["angle"]

    @property
    def flip_h(self) -> bool:
        """Returns whether the avatar decoration is flipped horizontally.

        Returns
        -------
        bool
            Whether the avatar decoration is flipped horizontally.
        """
        return self.__raw_avatar_decoration["flip_h"]

    @property
    def url(self) -> str:
        """Returns the url of the avatar decoration.

        Returns
        -------
        str
            The url of the avatar decoration.
        """
        return self.__raw_avatar_decoration["url"]


class PartialUser(Generic[PU]):
    def __init__(self, raw_user: PU, *, client: ClientManager) -> None:
        self._raw_user: PU = raw_user
        self._client: ClientManager = client

    @property
    def id(self) -> str:
        """Returns the id of the user."""
        return self._raw_user["id"]

    @deprecated
    @property
    def nickname(self) -> str | None:
        """Returns the nickname of the user.

        .. deprecated:: 0.6.0
            Use :meth:`mipac.models.lite.user.PartialUser.name` instead.

        Returns
        -------
        str | None
            The nickname of the user.
        """
        return self._raw_user["name"]

    @property
    def name(self) -> str | None:
        """Returns the nickname of the user.

        Returns
        -------
        str | None
            The nickname of the user.
        """
        return self._raw_user["name"]

    @property
    def username(self) -> str:
        """Returns the username of the user.

        Returns
        -------
        str
            The username of the user.
        """
        return self._raw_user["username"]

    @property
    def host(self) -> str | None:
        """Returns the host of the user.

        Returns
        -------
        str | None
            The host of the user.
        """
        return self._raw_user["host"]

    @property
    def avatar_url(self) -> str | None:
        """Returns the avatar url of the user.

        Returns
        -------
        str | None
            The avatar url of the user.
        """
        return self._raw_user["avatar_url"]

    @property
    def avatar_blurhash(self) -> str | None:
        """Returns the avatar blurhash of the user.

        Returns
        -------
        str | None
            The avatar blurhash of the user.
        """
        return self._raw_user["avatar_blurhash"]

    @property
    def avatar_decoration(self) -> list[AvatarDecoration]:
        """Returns the avatar decoration of the user.

        Returns
        -------
        list[AvatarDecoration]
            The avatar decoration of the user.
        """
        return [
            AvatarDecoration(data, client=self._client)
            for data in self._raw_user["avatar_decoration"]
        ]

    @property
    def is_bot(self) -> bool | None:
        """Returns whether the user is a bot.

        Returns
        -------
        bool | None
            Whether the user is a bot.
        """
        return self._raw_user.get("is_bot")

    @property
    def is_cat(self) -> bool | None:
        """Returns whether the user is a cat.

        Returns
        -------
        bool | None
            Whether the user is a cat.
        """
        return self._raw_user.get("is_cat")

    @property
    def instance(self) -> LiteInstance | None:
        """Returns the instance of the user.

        Returns
        -------
        LiteInstance | None
            The instance of the user.
        """
        raw_instance = self._raw_user.get("instance")
        return LiteInstance(raw_instance) if raw_instance else None

    @property
    def emojis(self) -> dict[str, str]:
        """Returns the emojis of the user.

        Returns
        -------
        dict[str, str]
            The emojis of the user.
        """
        return self._raw_user["emojis"]

    @property
    def online_status(self) -> IUserOnlineStatus:
        """Returns the online status of the user.

        Returns
        -------
        IUserOnlineStatus
            The online status of the user.
        """
        return self._raw_user["online_status"]

    @property
    def badge_roles(self) -> list[BadgeRole] | None:
        """Returns the badge roles of the user.

        Returns
        -------
        list[BadgeRole] | None
            The badge roles of the user.
        """
        return (
            [BadgeRole(data, client=self._client) for data in self._raw_user["badge_roles"]]
            if self._raw_user.get("badge_roles")
            else None
        )

    @property
    def api(self) -> UserManager:
        """Returns the user manager instance.

        Returns
        -------
        UserManager
            The user manager instance
        """
        return self._client._create_user_instance(self)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
