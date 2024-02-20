from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.drive import File, Folder
from mipac.types.drive import IFolder
from mipac.utils.format import remove_dict_missing
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientFileActionsInFolder(AbstractAction):
    """File actions in a folder"""

    def __init__(self, folder_id: str, *, session: HTTPClient, client: ClientManager):
        self._folder_id: str = folder_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(
        self,
        file: str,
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
        return await self._client.drive.files.action.create(
            file=file,
            name=name,
            comment=comment,
            is_sensitive=is_sensitive,
            force=force,
            folder_id=self._folder_id,
        )

    async def update(
        self,
        file_id: str,
        name: str | None = MISSING,
        is_sensitive: bool = MISSING,
        comment: str | None = MISSING,
    ):
        """Update a file

        Endpoint: `/api/drive/files/update`

        Parameters
        ----------
        file_id: str | None
            The id of the file to update, defaults to None
        name: str | None
            The name of the file, defaults to MISSING
        is_sensitive: bool
            Whether the file is sensitive or not, defaults to MISSING
        comment: str | None
            The comment of the file, defaults to MISSING

        Returns
        -------
        File
            The updated file
        """
        return await self._client.drive.files.action.update(
            file_id=file_id,
            name=name,
            is_sensitive=is_sensitive,
            comment=comment,
            folder_id=self._folder_id,
        )

    async def find(self, name: str) -> list[File]:
        """Find a file by its name

        Endpoint: `/api/drive/files/find`

        Parameters
        ----------
        name: str
            The name of the file to find

        Returns
        -------
        list[File]
            The found files
        """
        return await self._client.drive.files.action.find(name=name, folder_id=self._folder_id)

    async def upload_from_url(
        self,
        url: str,
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
        return await self._client.drive.files.action.upload_from_url(
            url=url,
            folder_id=self._folder_id,
            is_sensitive=is_sensitive,
            comment=comment,
            marker=marker,
            force=force,
        )


class SharedFolderActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def gets(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        folder_id: str,
    ) -> list[Folder]:
        """Get folders

        Endpoint: `/api/drive/folders`

        Parameters
        ----------
        limit: int
            The limit of folders to get, defaults to 10
        since_id: str | None
            The ID of the folder to get since, defaults to None
        until_id: str | None
            The ID of the folder to get until, defaults to None
        folder_id: str | None
            The ID of the folder to get, defaults to None

        Returns
        -------
        list[Folder]
            The found folders
        """
        data = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "folderId": folder_id,
        }
        raw_folders: list[IFolder] = await self._session.request(
            Route("POST", "/api/drive/folders"),
            auth=True,
            json=data,
        )

        return [Folder(raw_folder=raw_folder, client=self._client) for raw_folder in raw_folders]

    async def create(self, name: str | None = None, *, parent_id: str | None = None) -> Folder:
        """Create a new folder

        Endpoint: `/api/drive/folders/create`

        Parameters
        ----------
        name : str, optional
            The name of the folder, by default None
        parent_id : str, optional
            The parent ID of the folder, by default None

        Returns
        -------
        Folder
            The created folder
        """
        data = {"name": name, "parentId": parent_id}
        raw_created_folder: IFolder = await self._session.request(
            Route("POST", "/api/drive/folders/create"), auth=True, json=data
        )

        return Folder(raw_folder=raw_created_folder, client=self._client)

    async def delete(self, *, folder_id: str) -> bool:
        """Delete a folder

        Endpoint: `/api/drive/folders/delete`

        Parameters
        ----------
        folder_id : str, optional
            The ID of the folder, by default None

        Returns
        -------
        bool
            Whether the folder was deleted or not
        """
        res: bool = await self._session.request(
            Route("POST", "/api/drive/folders/delete"), auth=True, json={"folderId": folder_id}
        )

        return res

    async def update(
        self,
        name: str | None = MISSING,
        parent_id: str | None = MISSING,
        *,
        folder_id: str,
    ) -> Folder:
        """Update a folder

        Endpoint: `/api/drive/folders/update`

        Parameters
        ----------
        name : str, optional
            The name of the folder, by default MISSING
        parent_id : str, optional
            The parent ID of the folder, by default MISSING
        folder_id : str, optional
            The ID of the folder, by default None

        Returns
        -------
        Folder
            The updated folder
        """
        data = remove_dict_missing({"folderId": folder_id, "name": name, "parentId": parent_id})
        raw_updated_folder: IFolder = await self._session.request(
            Route("POST", "/api/drive/folders/update"), auth=True, json=data
        )

        return Folder(raw_folder=raw_updated_folder, client=self._client)


class ClientFolderActions(SharedFolderActions):
    def __init__(self, folder_id: str, *, session: HTTPClient, client: ClientManager):
        self.__folder_id: str = folder_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    @override
    async def gets(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        folder_id: str | None = None,
    ) -> list[Folder]:
        """Get folders

        Endpoint: `/api/drive/folders`

        Parameters
        ----------
        limit: int
            The limit of folders to get, defaults to 10
        since_id: str | None
            The ID of the folder to get since, defaults to None
        until_id: str | None
            The ID of the folder to get until, defaults to None
        folder_id: str | None
            The ID of the folder to get, defaults to None

        Returns
        -------
        list[Folder]
            The found folders
        """
        folder_id = folder_id or self.__folder_id

        return await super().gets(
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            folder_id=folder_id,
        )

    @override
    async def create(self, name: str | None = None, *, parent_id: str | None = None) -> Folder:
        """Create a new folder

        Endpoint: `/api/drive/folders/create`

        Parameters
        ----------
        name : str, optional
            The name of the folder, by default None
        parent_id : str, optional
            The parent ID of the folder, by default None

        Returns
        -------
        Folder
            The created folder
        """
        parent_id = parent_id or self.__folder_id

        return await super().create(name=name, parent_id=parent_id)

    @override
    async def delete(self, *, folder_id: str | None = None) -> bool:
        """Delete a folder

        Endpoint: `/api/drive/folders/delete`

        Parameters
        ----------
        folder_id : str, optional
            The ID of the folder, by default None

        Returns
        -------
        bool
            Whether the folder was deleted or not
        """
        folder_id = folder_id or self.__folder_id

        return await super().delete(folder_id=folder_id)

    @override
    async def update(
        self,
        name: str | None = MISSING,
        parent_id: str | None = MISSING,
        *,
        folder_id: str | None = None,
    ) -> Folder:
        """Update a folder

        Endpoint: `/api/drive/folders/update`

        Parameters
        ----------
        name : str, optional
            The name of the folder, by default MISSING
        parent_id : str, optional
            The parent ID of the folder, by default MISSING
        folder_id : str, optional
            The ID of the folder, by default None

        Returns
        -------
        Folder
            The updated folder
        """
        folder_id = folder_id or self.__folder_id

        return await super().update(name=name, parent_id=parent_id, folder_id=folder_id)


class FolderActions(SharedFolderActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def find(self, name: str, parent_id: str | None = None) -> list[Folder]:
        """Find folders

        Endpoint: `/api/drive/folders/find`

        Parameters
        ----------
        name : str
            The name of the folder
        parent_id : str, optional
            The parent ID of the folder, by default None

        Returns
        -------
        list[Folder]
            The found folders
        """

        data = {"name": name, "parentId": parent_id}
        raw_folders: list[IFolder] = await self._session.request(
            Route("POST", "/api/drive/folders/find"),
            auth=True,
            json=data,
        )

        return [Folder(raw_folder=raw_folder, client=self._client) for raw_folder in raw_folders]

    async def show(self, folder_id: str) -> Folder:
        """Show a folder

        Endpoint: `/api/drive/folders/show`

        Parameters
        ----------
        folder_id : str
            The ID of the folder

        Returns
        -------
        Folder
            The found folder
        """
        raw_folder: IFolder = await self._session.request(
            Route("POST", "/api/drive/folders/show"),
            auth=True,
            json={"folderId": folder_id},
        )

        return Folder(raw_folder=raw_folder, client=self._client)
