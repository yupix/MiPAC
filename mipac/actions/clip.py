from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.clip import Clip
from mipac.models.note import Note
from mipac.types.clip import IClip
from mipac.types.note import INote
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ClientClipActions(AbstractAction):
    def __init__(self, *, clip_id: str | None = None, session: HTTPClient, client: ClientManager):
        self._clip_id = clip_id
        self._session = session
        self._client = client

    async def get_notes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
        clip_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """Get notes from a clip
        Parameters
        ----------
        clip_id : str | None, optional, by default None
            The clip id
        limit : int, optional, by default 10
            The number of notes to get
        since_id : str | None, optional, by default None
            The note id to get notes after
        until_id : str | None, optional, by default None
            The note id to get notes before
        get_all : bool, optional, by default False
            Whether to get all notes

        Yields
        ------
        AsyncGenerator[Note, None]
            The notes
        """

        clip_id = self._clip_id or clip_id

        if clip_id is None:
            raise ValueError("clip_id is required")

        if limit > 100:
            raise ValueError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {"clipId": clip_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/clips/notes"), json=body, auth=True
        )

        while True:
            clips = await pagination.next()
            for raw_clip in clips:
                yield Note(raw_clip, client=self._client)

            if get_all is False or pagination.is_final:
                break

    async def add_note(self, note_id: str, clip_id: str | None = None) -> bool:
        """Add a note to a clip

        Parameters
        ----------
        clip_id : str | None, optional, by default None
            The clip id
        note_id : str
            The note id

        Returns
        -------
        bool
            True if the note was added to the clip, False otherwise
        """
        clip_id = self._clip_id or clip_id

        if clip_id is None:
            raise ValueError("clip_id is required")

        body = {"clipId": clip_id, "noteId": note_id}
        result: bool = await self._session.request(
            Route("POST", "/api/clips/add-note"), json=body, auth=True
        )
        return result

    async def remove_note(self, note_id: str, clip_id: str | None) -> bool:
        """Remove a note from a clip

        Parameters
        ----------
        clip_id : str | None, optional, by default None
            The clip id
        note_id : str
            The note id

        Returns
        -------
        bool
            True if the note was removed from the clip, False otherwise
        """
        clip_id = self._clip_id or clip_id

        if clip_id is None:
            raise ValueError("clip_id is required")

        body = {"clipId": clip_id, "noteId": note_id}
        result: bool = await self._session.request(
            Route("POST", "/api/clips/remove-note"), json=body, auth=True
        )
        return result

    async def delete(self, clip_id: str | None = None) -> bool:
        """Delete a clip

        Parameters
        ----------
        clip_id : str | None, optional, by default None
            The clip id

        Returns
        -------
        bool
            True if the clip was deleted, False otherwise
        """
        clip_id = self._clip_id or clip_id

        if clip_id is None:
            raise ValueError("clip_id is required")

        body = {"clipId": clip_id}
        result: bool = await self._session.request(
            Route("POST", "/api/clips/delete"), json=body, auth=True
        )
        return result

    async def update(
        self,
        name: str,
        is_public: bool | None = None,
        description: str | None = None,
        clip_id: str | None = None,
    ) -> Clip:
        """Update a clip

        Parameters
        ----------
        clip_id : str | None, optional, by default None
            The clip id
        name : str
            The clip name
        is_public : bool, optional
            Whether the clip is public, by default None
        description : str, optional
            The clip description, by default None

        Returns
        -------
        bool
            True if the clip was updated, False otherwise
        """

        clip_id = self._clip_id or clip_id

        if clip_id is None:
            raise ValueError("clip_id is required")

        body = {"clipId": clip_id, "name": name, "isPublic": is_public, "description": description}
        result: IClip = await self._session.request(
            Route("POST", "/api/clips/update"), json=body, auth=True
        )
        return Clip(result, client=self._client)


class ClipActions(ClientClipActions):
    def __init__(self, *, clip_id: str | None = None, session: HTTPClient, client: ClientManager):
        super().__init__(clip_id=clip_id, session=session, client=client)

    async def get_my_favorites(self):
        """Get my favorite clips

        Returns
        -------
        list[Clip]
            The favorite clips
        """
        clips: list[INote] = await self._session.request(
            Route("POST", "/api/clips/my-favorites"), auth=True
        )
        return [Note(raw_clip, client=self._client) for raw_clip in clips]

    async def create(
        self, name: str, is_public: bool = False, description: str | None = None
    ) -> Clip:
        """Create a clip

        Parameters
        ----------
        name : str
            The clip name
        is_public : bool, optional
            Whether the clip is public, by default False
        description : str, optional
            The clip description, by default None

        Returns
        -------
        Clip
            The created clip
        """
        body = {"name": name, "isPublic": is_public, "description": description}
        clip: IClip = await self._session.request(
            Route("POST", "/api/clips/create"), json=body, auth=True
        )
        return Clip(clip, client=self._client)

    async def get_list(self) -> list[Clip]:
        """Get my clips

        Returns
        -------
        list[Clip]
            The clips
        """
        clips: list[IClip] = await self._session.request(
            Route("POST", "/api/clips/list"), auth=True
        )
        return [Clip(raw_clip, client=self._client) for raw_clip in clips]

    async def get(self, clip_id: str) -> Clip:
        """Get a clip

        Parameters
        ----------
        clip_id : str
            The clip id

        Returns
        -------
        Clip
            The clip
        """
        body = {"clipId": clip_id}
        clip: IClip = await self._session.request(
            Route("POST", "/api/clips/show"), json=body, auth=True
        )
        return Clip(clip, client=self._client)
