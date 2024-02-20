from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.user import PartialUser
from mipac.types.clip import IClip

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.clip import ClientClipManager


class Clip:
    def __init__(self, raw_clip: IClip, *, client: ClientManager) -> None:
        self.__clip: IClip = raw_clip
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """The clip id"""
        return self.__clip["id"]

    @property
    def created_at(self) -> str:
        """The time the clip was created"""
        return self.__clip["created_at"]

    @property
    def last_clipped_at(self) -> str:
        """The last time the clip was clipped"""
        return self.__clip["last_clipped_at"]

    @property
    def user_id(self) -> str:
        """The user id who created the clip"""
        return self.__clip["user_id"]

    @property
    def user(self) -> PartialUser:
        """The user who created the clip"""
        return PartialUser(self.__clip["user"], client=self.__client)

    @property
    def name(self) -> str:
        """The clip name"""
        return self.__clip["name"]

    @property
    def description(self) -> str | None:
        """The clip description"""
        return self.__clip["description"]

    @property
    def is_public(self) -> bool:
        """Whether the clip is public"""
        return self.__clip["is_public"]

    @property
    def favorited_count(self) -> int:
        """The number of times the clip has been favorited"""
        return self.__clip["favorited_count"]

    @property
    def is_favorited(self) -> bool:
        """Whether the clip is favorited"""
        return self.__clip["is_favorited"]

    @property
    def api(self) -> ClientClipManager:
        return self.__client._get_client_clip_instance(clip_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self.__clip.get(key)
