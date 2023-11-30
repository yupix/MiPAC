from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, NotRequired, TypedDict

if TYPE_CHECKING:
    from mipac.models.lite.user import PartialUser


__all__ = ("IFileProperties", "FolderPayload", "IDriveFile")

IDriveSort = Literal["+createdAt", "-createdAt", "+name", "-name", "+size", "-size"]


class IDriveStatus(TypedDict):
    capacity: int
    usage: int


class IFileProperties(TypedDict):
    """
    プロパティー情報
    """

    width: NotRequired[int]
    height: NotRequired[int]
    orientation: NotRequired[int]
    avg_color: NotRequired[str]


class FolderPayload(TypedDict):
    """
    フォルダーの情報
    """

    id: str
    created_at: str
    name: str
    parent_id: str | None
    folders_count: NotRequired[int]
    files_count: NotRequired[int]
    parent: NotRequired[FolderPayload | None]


class IDriveFile(TypedDict):
    """
    ファイル情報
    """

    id: str
    created_at: str
    name: str
    type: str
    md5: str
    size: int
    is_sensitive: bool
    blurhash: str | None
    properties: IFileProperties
    url: str
    thumbnail_url: str | None
    comment: str | None
    folder_id: str | None
    folder: NotRequired[FolderPayload | None]
    user_id: str | None
    user: NotRequired[PartialUser | None]
