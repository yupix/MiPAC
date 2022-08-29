from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.core.models.drive import RawFolder

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.manager.drive import FolderManager
    from mipac.types import IDriveFile, IFileProperties

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
    def __init__(self, raw_data: RawFolder, client: ClientActions):
        self.__raw_data = raw_data
        self.__client: ClientActions = client

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def folders_count(self):
        return self.__raw_data.folders_count

    @property
    def parent_id(self):
        return self.__raw_data.parent_id

    @property
    def parent(self):
        return self.__raw_data.parent

    @property
    def action(self) -> FolderManager:
        return self.__client.drive._get_folder_instance(self.id)


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
