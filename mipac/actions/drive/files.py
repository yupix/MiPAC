from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import File
from mipac.models.note import Note
from mipac.types.drive import IDriveFile, IDriveSort
from mipac.types.note import INote
from mipac.utils.format import bool_to_string, remove_dict_missing
from mipac.utils.util import MISSING, credentials_required

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientFileActions(AbstractAction):
    def __init__(self, file_ids: str | None = None, *, session: HTTPClient, client: ClientManager):
        self.__file_ids: str | None = file_ids
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_attached_notes(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        file_id: str | None = None,
    ) -> list[Note]:
        """Get the attached notes of a file

        Endpoint: `/api/drive/files/attached-notes`

        Parameters
        ----------
        since_id: str | None
            The id of the note to start from, defaults to None
        until_id: str | None
            The id of the note to end at, defaults to None
        limit: int
            The amount of notes to get, defaults to 10
        file_id: str | None
            The id of the file to get notes from, defaults to None

        Returns
        -------
        list[Note]
            The attached notes of the file
        """

        file_id = file_id or self.__file_ids

        data = {
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "fileId": file_id,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/drive/files/attached-notes"), json=data, auth=True
        )
        return [Note(raw_note, client=self._client) for raw_note in raw_notes]

    async def delete(self, *, file_id: str | None = None) -> bool:
        """Delete a file

        Endpoint: `/api/drive/files/delete`

        Parameters
        ----------
        file_id: str | None
            The id of the file to delete, defaults to None

        Returns
        -------
        bool
            Whether the file was deleted or not
        """

        file_id = file_id or self.__file_ids

        data = {"fileId": file_id}

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/delete"), json=data, auth=True
        )
        return res

    async def update(
        self,
        folder_id: str | None = MISSING,
        name: str | None = MISSING,
        is_sensitive: bool = MISSING,
        comment: str | None = MISSING,
        *,
        file_id: str | None = None,
    ):
        """Update a file

        Endpoint: `/api/drive/files/update`

        Parameters
        ----------
        folder_id: str | None
            The id of the folder to update the file to, defaults to MISSING
        name: str | None
            The name of the file, defaults to MISSING
        is_sensitive: bool
            Whether the file is sensitive or not, defaults to MISSING
        comment: str | None
            The comment of the file, defaults to MISSING
        file_id: str | None
            The id of the file to update, defaults to None

        Returns
        -------
        File
            The updated file
        """

        file_id = file_id or self.__file_ids

        data = remove_dict_missing(
            {
                "fileId": file_id,
                "folderId": folder_id,
                "name": name,
                "isSensitive": is_sensitive,
                "comment": comment,
            }
        )

        res: IDriveFile = await self._session.request(
            Route("POST", "/api/drive/files/update"), json=data, auth=True
        )
        return File(res, client=self._client)


class FileActions(ClientFileActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    @credentials_required
    async def get_files(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        folder_id: str | None = None,
        type: str | None = None,
        sort: IDriveSort | None = None,
    ) -> list[File]:
        """Get the files of the drive

        Endpoint: `/api/drive/files`

        Parameters
        ----------
        limit: int
            The amount of files to get, defaults to 10
        since_id: str | None
            The id of the file to start from, defaults to None
        until_id: str | None
            The id of the file to end at, defaults to None
        folder_id: str | None
            The id of the folder to get files from, defaults to None
        type: str | None
            The type of file to get, defaults to None
        sort: IDriveSort | None
            The way to sort the files, defaults to None

        Returns
        -------
        list[File]
            The files of the drive
        """

        data = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "folderId": folder_id,
            "type": type,
            "sort": sort,
        }

        raw_files: list[IDriveFile] = await self._session.request(
            Route("POST", "/api/drive/files"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in raw_files]

    async def get_attached_notes(
        self,
        file_id: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
    ) -> list[Note]:
        """Get the attached notes of a file

        Endpoint: `/api/drive/files/attached-notes`

        Parameters
        ----------
        file_id: str
            The id of the file to get notes from
        since_id: str | None
            The id of the note to start from, defaults to None
        until_id: str | None
            The id of the note to end at, defaults to None
        limit: int
            The amount of notes to get, defaults to 10

        Returns
        -------
        list[Note]
            The attached notes of the file
        """

        return await super().get_attached_notes(
            since_id=since_id, until_id=until_id, limit=limit, file_id=file_id
        )

    @credentials_required
    async def check_existence(self, md5: str) -> bool:
        """Check if a file exists in the drive

        Endpoint: `/api/drive/files/check-existence`

        Parameters
        ----------
        md5: str
            The md5 of the file to check

        Returns
        -------
        bool
            Whether the file exists or not
        """

        data = {"md5": md5}

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/check-existence"), json=data, auth=True
        )
        return res

    async def create(
        self,
        file,
        folder_id: str | None = None,
        name: str | None = None,
        comment: str | None = None,
        is_sensitive: bool = False,
        force: bool = False,
    ) -> File:
        """Upload a file to the drive

        Endpoint: `/api/drive/files/create`

        Parameters
        ----------
        file: str
            The file to upload
        folder_id: str | None
            The id of the folder to upload the file to, defaults to None
        name: str | None
            The name of the file, defaults to None
        comment: str | None
            The comment of the file, defaults to None
        is_sensitive: bool
            Whether the file is sensitive or not, defaults to False
        force: bool
            Whether to force upload the file or not, defaults to False

        Returns
        -------
        File
            The uploaded file
        """

        file_byte = open(file, "rb") if file else None

        data = {
            "folderId": folder_id,
            "name": name,
            "comment": comment,
            "isSensitive": bool_to_string(is_sensitive),
            "force": bool_to_string(force),
            "file": file_byte,
        }
        res: IDriveFile = await self._session.request(
            Route("POST", "/api/drive/files/create"),
            data=data,
            auth=True,
            lower=True,
        )
        return File(res, client=self._client)

    async def delete(self, file_id: str) -> bool:
        """Delete a file

        Endpoint: `/api/drive/files/delete`

        Parameters
        ----------
        file_id: str
            The id of the file to delete

        Returns
        -------
        bool
            Whether the file was deleted or not
        """

        return await super().delete(file_id=file_id)

    async def find_by_hash(self, md5: str) -> list[File]:
        """Find a file by its hash

        Endpoint: `/api/drive/files/find-by-hash`

        Parameters
        ----------
        md5: str
            The md5 of the file to find

        Returns
        -------
        list[File]
            The found files
        """

        data = {"md5": md5}

        raw_files: list[IDriveFile] = await self._session.request(
            Route("POST", "/api/drive/files/find-by-hash"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in raw_files]

    async def find(self, name: str, folder_id:str|None=None) -> list[File]:
        """Find a file by its name

        Endpoint: `/api/drive/files/find`

        Parameters
        ----------
        name: str
            The name of the file to find
        folder_id: str | None
            The id of the folder to find the file in, defaults to None

        Returns
        -------
        list[File]
            The found files
        """

        data = {"name": name, "folderId": folder_id}

        res: list[IDriveFile] = await self._session.request(
            Route("POST", "/api/drive/files/find"), json=data, auth=True
        )
        return [File(raw_file, client=self._client) for raw_file in res]

    async def show(self, file_id: str, url: str | None = None) -> File:
        """Show a file

        Endpoint: `/api/drive/files/show`

        Parameters
        ----------
        file_id: str
            The id of the file to show
        url: str | None
            The url of the file to show, defaults to None

        Returns
        -------
        File
            The shown file
        """

        data = {"fileId": file_id, "url": url}

        res: IDriveFile = await self._session.request(
            Route("POST", "/api/drive/files/show"), json=data, auth=True
        )
        return File(res, client=self._client)

    async def update(
        self,
        file_id: str,
        folder_id: str | None = None,
        name: str | None = None,
        is_sensitive: bool = False,
        comment: str | None = None,
    ) -> File:
        """Update a file

        Endpoint: `/api/drive/files/update`

        Parameters
        ----------
        file_id: str
            The id of the file to update
        folder_id: str | None
            The id of the folder to update the file to, defaults to None
        name: str | None
            The name of the file, defaults to None
        is_sensitive: bool
            Whether the file is sensitive or not, defaults to False
        comment: str | None
            The comment of the file, defaults to None

        Returns
        -------
        File
            The updated file
        """

        return await super().update(
            file_id=file_id,
            folder_id=folder_id,
            name=name,
            is_sensitive=is_sensitive,
            comment=comment,
        )

    async def upload_from_url(
        self,
        url: str,
        folder_id: str | None = None,
        is_sensitive: bool = False,
        comment: str | None = None,
        marker: str | None = None,
        force: bool = False,
    ):
        """Upload a file to the drive from a url

        Endpoint: `/api/drive/files/upload-from-url`

        Parameters
        ----------
        url: str
            The url of the file to upload
        folder_id: str | None
            The id of the folder to upload the file to, defaults to None
        is_sensitive: bool
            Whether the file is sensitive or not, defaults to False
        comment: str | None
            The comment of the file, defaults to None
        marker: str | None
            The marker of the file, defaults to None
        force: bool
            Whether to force upload the file or not, defaults to False

        Returns
        -------
        bool
            Whether the file was uploaded or not
        """

        data = {
            "url": url,
            "folderId": folder_id,
            "isSensitive": is_sensitive,
            "comment": comment,
            "marker": marker,
            "force": force,
        }

        res: bool = await self._session.request(
            Route("POST", "/api/drive/files/upload-from-url"), json=data, auth=True
        )
        return res
