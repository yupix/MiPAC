from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import DriveStatus
from mipac.types.drive import IDriveStatus

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class DriveActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_status(self) -> DriveStatus:
        """Get the status of the drive

        Returns
        -------
        DriveStatus
            The status of the drive
        """

        res: IDriveStatus = await self.__session.request(Route("POST", "/api/drive"), auth=True)
        return DriveStatus(raw_drive_status=res, client=self.__client)
