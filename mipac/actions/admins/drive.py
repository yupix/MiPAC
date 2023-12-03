from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import File
from mipac.types.drive import IFile

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminDriveActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def clean_remote_files(self) -> bool:
        """Clean remote files

        Endpoint: `/api/admin/drive/clean-remote-files`

        Returns
        -------
        bool
            Whether the remote files were cleaned
        """

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/drive/clean-remote-files"), auth=True
        )
        return res

    async def cleanup(self) -> bool:
        """Clean up the drive

        Endpoint: `/api/admin/drive/cleanup`

        Returns
        -------
        bool
            Whether the drive was cleaned up
        """

        res: bool = await self.__session.request(
            Route("POST", "/api/admin/drive/cleanup"), auth=True
        )
        return res

    async def get_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        user_id: str | None = None,
        type: str | None = None,
        origin: Literal["combined", "local", "remote"] = "local",
        hostname: str | None = None,
    ) -> list[File]:
        """Get all files

        Endpoint: `/api/admin/drive/files`

        Parameters
        ----------
        limit: int
            The number of files to get
        since_id: str
            The id of the file to start from
        until_id: str
            The id of the file to end at
        type: str
            The type of file to get
        user_id: str
            The id of the user to get files from
        origin: Literal['combined', 'local', 'remote']
            The origin of the files
        hostname: str
            The hostname of the files

        Returns
        -------
        list[File]
            A list of files
        """

        data = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "type": type,
            "userId": user_id,
            "origin": origin,
            "hostname": hostname,
        }
        raw_files: list[IFile] = await self.__session.request(
            Route("POST", "/api/admin/drive/files"), auth=True, json=data
        )
        return [File(raw_file=file, client=self.__client) for file in raw_files]

    async def show_file(self, file_id: str, url: str | None = None):
        """Show a file

        Endpoint: `/api/admin/drive/files/show`

        Parameters
        ----------
        file_id: str
            The id of the file to show
        url: str
            The url of the file to show

        Returns
        -------
        dict[str, Any]
            The file
        """

        data = {
            "fileId": file_id,
            "url": url,
        }
        # TODO: IFileではなく、ほぼほぼデータベースの中身が返ってくるのでそれに合わせた型とモデルを作る
        raw_file: dict[str, Any] = await self.__session.request(
            Route("POST", "/api/admin/drive/show-file"), auth=True, json=data
        )
        return raw_file
