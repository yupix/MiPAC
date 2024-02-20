from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.drive import File
from mipac.models.lite.user import PartialUser
from mipac.types.gallery import IGalleryPost
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class GalleryPost:
    def __init__(self, raw_gallery: IGalleryPost, *, client: ClientManager) -> None:
        self._raw_gallery: IGalleryPost = raw_gallery
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self._raw_gallery["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._raw_gallery["created_at"])

    @property
    def updated_at(self) -> datetime:
        return str_to_datetime(self._raw_gallery["updated_at"])

    @property
    def user_id(self) -> str:
        return self._raw_gallery["user_id"]

    @property
    def user(self) -> PartialUser:
        return PartialUser(self._raw_gallery["user"], client=self.__client)

    @property
    def title(self) -> str:
        return self._raw_gallery["title"]

    @property
    def description(self) -> str | None:
        return self._raw_gallery["description"]

    @property
    def file_ids(self) -> list[str]:
        return self._raw_gallery["file_ids"]

    @property
    def files(self) -> list[File]:
        return [File(file, client=self.__client) for file in self._raw_gallery["files"]]

    @property
    def tags(self) -> list[str] | None:
        return self._raw_gallery.get("tags")

    @property
    def is_sensitive(self) -> bool:
        return self._raw_gallery["is_sensitive"]

    @property
    def liked_count(self) -> int:
        return self._raw_gallery["liked_count"]

    @property
    def is_liked(self) -> bool | None:
        return self._raw_gallery.get("is_liked")

    def _get(self, key: str) -> Any | None:
        return self._raw_gallery.get(key)
