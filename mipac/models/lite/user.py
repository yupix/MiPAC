from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.models.lite.instance import LiteInstance
from mipac.types.user import IBadgeRole, IPartialUser, IUserOnlineStatus

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.user import UserManager

T = TypeVar("T", bound=IBadgeRole)
PU = TypeVar("PU", bound=IPartialUser)


class BadgeRole(AbstractModel, Generic[T]):
    def __init__(self, data: T, *, client: ClientManager) -> None:
        self._data: T = data
        self._client = client

    @property
    def name(self) -> str:
        """Returns the name of the badge role."""
        return self._data["name"]

    @property
    def icon_url(self) -> str | None:
        """Returns the icon url of the badge role."""
        return self._data["icon_url"]

    @property
    def display_order(self) -> int:
        """Returns the display order of the badge role."""
        return self._data["display_order"]


class PartialUser(AbstractModel, Generic[PU]):
    def __init__(self, raw_user: PU, *, client: ClientManager) -> None:
        self._raw_user: PU = raw_user
        self._client: ClientManager = client

    @property
    def id(self) -> str:
        """Returns the id of the user."""
        return self._raw_user["id"]

    @property
    def nickname(self) -> str | None:
        """Returns the nickname of the user."""
        return self._raw_user["name"]

    @property
    def username(self) -> str:
        """Returns the username of the user."""
        return self._raw_user["username"]

    @property
    def host(self) -> str | None:
        """Returns the host of the user."""
        return self._raw_user["host"]

    @property
    def avatar_url(self) -> str:
        """Returns the avatar url of the user."""
        return self._raw_user["avatar_url"]

    @property
    def avatar_blurhash(self) -> str:
        """Returns the avatar blurhash of the user."""
        return self._raw_user["avatar_blurhash"]

    @property
    def is_bot(self) -> bool:
        """Returns whether the user is a bot."""
        return self._raw_user["is_bot"]

    @property
    def is_cat(self) -> bool:
        """Returns whether the user is a cat."""
        return self._raw_user["is_cat"]

    @property
    def instance(self) -> LiteInstance | None:
        """Returns the instance of the user."""
        raw_instance = self._raw_user.get("instance")
        return LiteInstance(raw_instance) if raw_instance else None

    @property
    def emojis(self) -> dict[str, str]:
        """Returns the emojis of the user."""
        return self._raw_user["emojis"]

    @property
    def online_status(self) -> IUserOnlineStatus:
        """Returns the online status of the user."""
        return self._raw_user["online_status"]

    @property
    def badge_roles(self) -> list[BadgeRole]:
        """Returns the badge roles of the user."""
        return [
            BadgeRole(data, client=self._client) for data in self._raw_user.get("badge_roles", [])
        ]

    @property
    def api(self) -> UserManager:
        return self._client._create_user_instance(self)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
