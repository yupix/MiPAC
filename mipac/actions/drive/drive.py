from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import DriveStatus, File
from mipac.types.drive import IDriveStatus, IFile

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class DriveActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_status(self) -> DriveStatus:
        """Get the status of the drive

        Endpoint: `/api/drive`

        Returns
        -------
        DriveStatus
            The status of the drive
        """

        res: IDriveStatus = await self.__session.request(Route("POST", "/api/drive"), auth=True)
        return DriveStatus(raw_drive_status=res, client=self.__client)

    async def stream(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        type: str | None = None,
    ) -> list[File]:
        """Stream files from the drive

        Endpoint: `/api/drive/stream`

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

        Returns
        -------
        list[File]
            A list of files
        """

        params = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "type": type,
        }
        raw_files: list[IFile] = await self.__session.request(
            Route("POST", "/api/drive/stream"), auth=True, json=params
        )

        return [File(raw_file=raw_file, client=self.__client) for raw_file in raw_files]
