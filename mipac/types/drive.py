from __future__ import annotations

from typing import Any, Optional, TypedDict

__all__ = ('IFileProperties', 'FolderPayload', 'IDriveFile')


class IFileProperties(TypedDict):
    """
    プロパティー情報
    """

    width: int
    height: int
    avg_color: Optional[str]


class FolderPayload(TypedDict):
    """
    フォルダーの情報
    """

    id: str
    created_at: str
    name: str
    folders_count: int
    files_count: int
    parent_id: str
    parent: dict[str, Any]


class IDriveFile(TypedDict):
    """
    ファイル情報
    """

    id: str
    created_at: str
    is_sensitive: bool
    name: str
    thumbnail_url: str
    url: str
    type: str
    size: int
    md5: str
    blurhash: str
    properties: IFileProperties
