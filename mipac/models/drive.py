from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.types import FolderPayload, IDriveFile, IFileProperties

__all__ = ['FileProperties', 'File', 'Folder']


class FileProperties:
    def __init__(self, properties: IFileProperties) -> None:
        self.__properties: IFileProperties = properties

    @property
    def width(self) -> Optional[int]:
        return self.__properties['width']

    @property
    def height(self) -> int:
        return self.__properties['height']

    @property
    def avg_color(self) -> Optional[str]:
        return self.__properties['avg_color']


class Folder:
    def __init__(self, folder: FolderPayload, client: ClientActions):
        self.__folder: FolderPayload = folder
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        """フォルダのID"""
        return self.__folder['id']

    @property
    def created_at(self) -> str:  # TODO: 型
        """フォルダの作成日時"""
        return self.__folder['created_at']

    @property
    def name(self) -> str:
        """フォルダ名"""
        return self.__folder['name']

    @property
    def folders_count(self) -> int:
        """フォルダ内のフォルダ数"""
        return self.__folder['folders_count']

    @property
    def files_count(self) -> int:
        """フォルダ内のファイル数"""
        return self.__folder['files_count']

    @property
    def parent_id(self) -> str:
        return self.__folder['parent_id']

    @property
    def parent(self) -> dict[str, Any]:
        return self.__folder['parent']


class File:
    def __init__(self, file: IDriveFile, *, client: ClientActions):
        self.__file: IDriveFile = file
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__file['id']

    @property
    def created_at(self):
        return self.__file['created_at']

    @property
    def is_sensitive(self) -> bool:
        return self.__file['is_sensitive']

    @property
    def name(self) -> str:
        return self.__file['name']

    @property
    def thumbnail_url(self) -> str:
        return self.__file['thumbnail_url']

    @property
    def url(self) -> str:
        return self.__file['url']

    @property
    def type(self) -> str:
        return self.__file['type']

    @property
    def size(self) -> int:
        return self.__file['size']

    @property
    def md5(self) -> str:
        return self.__file['md5']

    @property
    def blurhash(self) -> str:
        return self.__file['blurhash']

    @property
    def properties(self) -> FileProperties:
        return FileProperties(self.__file['properties'])
