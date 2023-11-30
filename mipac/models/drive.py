from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.abstract.model import AbstractModel
from mipac.types.drive import IDriveStatus

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.drive import ClientFileManager, ClientFolderManager
    from mipac.types import FolderPayload, IDriveFile, IFileProperties

__all__ = ["FileProperties", "File", "Folder"]


class DriveStatus:
    def __init__(self, raw_drive_status: IDriveStatus, *, client: ClientManager) -> None:
        self.__raw_drive_status: IDriveStatus = raw_drive_status
        self.__client: ClientManager = client

    @property
    def capacity(self) -> int:
        """Total capacity of the drive in bytes

        Returns
        -------
        int
            Total capacity of the drive in bytes
        """
        return self.__raw_drive_status["capacity"]

    @property
    def usage(self) -> int:
        """Total usage of the drive in bytes

        Returns
        -------
        int
            Total usage of the drive in bytes
        """
        return self.__raw_drive_status["usage"]


class FileProperties(AbstractModel):
    def __init__(self, properties: IFileProperties) -> None:
        self.__properties: IFileProperties = properties

    @property
    def width(self) -> int | None:
        return self.__properties["width"]

    @property
    def height(self) -> int:
        return self.__properties["height"]

    @property
    def avg_color(self) -> str | None:
        return self.__properties["avg_color"]


class Folder(AbstractModel):
    def __init__(self, folder: FolderPayload, client: ClientManager):
        self.__folder: FolderPayload = folder
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """フォルダのID"""
        return self.__folder["id"]

    @property
    def created_at(self) -> str:  # TODO: 型
        """フォルダの作成日時"""
        return self.__folder["created_at"]

    @property
    def name(self) -> str:
        """フォルダ名"""
        return self.__folder["name"]

    @property
    def folders_count(self) -> int:
        """フォルダ内のフォルダ数"""
        return self.__folder["folders_count"]

    @property
    def files_count(self) -> int:
        """フォルダ内のファイル数"""
        return self.__folder["files_count"]

    @property
    def parent_id(self) -> str:
        return self.__folder["parent_id"]

    @property
    def parent(self) -> dict[str, Any]:
        return self.__folder["parent"]

    @property
    def api(self) -> ClientFolderManager:
        return self.__client.drive._get_client_folder_instance(folder_id=self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Folder) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class File(AbstractModel):
    def __init__(self, file: IDriveFile, *, client: ClientManager):
        self.__file: IDriveFile = file
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__file["id"]

    @property
    def created_at(self):
        return self.__file["created_at"]

    @property
    def is_sensitive(self) -> bool:
        return self.__file["is_sensitive"]

    @property
    def name(self) -> str:
        return self.__file["name"]

    @property
    def thumbnail_url(self) -> str:
        return self.__file["thumbnail_url"]

    @property
    def url(self) -> str:
        return self.__file["url"]

    @property
    def type(self) -> str:
        return self.__file["type"]

    @property
    def size(self) -> int:
        return self.__file["size"]

    @property
    def md5(self) -> str:
        return self.__file["md5"]

    @property
    def blurhash(self) -> str:
        return self.__file["blurhash"]

    @property
    def properties(self) -> FileProperties:
        return FileProperties(self.__file["properties"])

    @property
    def api(self) -> ClientFileManager:
        return self.__client.drive._get_client_file_instance(file_id=self.id, url=self.url)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, File) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
