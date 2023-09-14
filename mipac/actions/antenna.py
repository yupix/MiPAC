from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.antenna import Antenna
from mipac.models.note import Note
from mipac.types.antenna import IAntenna, IAntennaReceiveSource
from mipac.types.note import INote
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class ClientAntennaActions(AbstractAction):
    def __init__(
        self, *, antenna_id: str | None = None, session: HTTPClient, client: ClientManager
    ):
        self._antenna_id: str | None = antenna_id
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, antenna_id: str | None = None) -> bool:
        """
        Delete antenna from identifier

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier

        Raises
        ------
        ParameterError
            antenna id is required
        Returns
        -------
        bool
            success or failure
        """
        antenna_id = antenna_id or self._antenna_id
        if antenna_id is None:
            raise ParameterError("antenna id is required")

        body = {"antennaId": antenna_id}
        res: bool = await self._session.request(
            Route("POST", "/api/antennas/delete"), auth=True, json=body
        )
        return res

    async def show(self, antenna_id: str | None = None) -> Antenna:
        """Show antenna from identifier

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier, by default None

        Returns
        -------
        Antenna
            antenna object

        Raises
        ------
        ParameterError
            antenna id is required
        """
        antenna_id = antenna_id or self._antenna_id
        if antenna_id is None:
            raise ParameterError("antenna id is required")

        body = {"antennaId": antenna_id}
        res_antenna: IAntenna = await self._session.request(
            Route("POST", "/api/antennas/show"), auth=True, json=body
        )
        return Antenna(res_antenna, client=self._client)

    async def get_notes(
        self,
        antenna_id: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: str | None = None,
        until_date: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[Note, None]:
        antenna_id = antenna_id or self._antenna_id
        if antenna_id is None:
            raise ParameterError("antenna id is required")

        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = remove_dict_empty(
            {
                "antennaId": antenna_id,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
                "sinceDate": since_date,
                "untilDate": until_date,
            }
        )

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/antennas/notes"), json=body
        )

        while True:
            res_notes = await pagination.next()
            for res_note in res_notes:
                yield Note(res_note, client=self._client)

            if get_all is False or pagination.is_final:
                break

    async def update(
        self,
        name: str,
        src: IAntennaReceiveSource,
        keywords: list[list[str]],
        exclude_keywords: list[list[str]],
        users: list[str],
        case_sensitive: bool,
        with_replies: bool,
        with_file: bool,
        notify: bool,
        user_list_id: str | None = None,
        antenna_id: str | None = None,
    ) -> Antenna:
        """Update an antenna.

        Parameters
        ----------
        name : str
            Name of the antenna.
        src : IAntennaReceiveSource
            Receive source of the antenna.
        keywords : list[list[str]]
            Receive keywords.
        exclude_keywords : list[list[str]]
            Excluded keywords.
        users : list[str]
            List of target user ID. Required when selecting 'users' as the receive source.
        case_sensitive : bool
            Whether to differentiate between uppercase and lowercase letters.
        with_replies : bool
            Whether to include replies.
        with_file : bool
            Whether to limit to notes with attached files.
        notify : bool
            Whether to notify for new notes.
        user_list_id : str | None, default None
            List of user IDs when selecting 'users' as the receive source for the antenna.

        Returns
        -------
        Antenna
            The created antenna.
        """

        antenna_id = antenna_id or self._antenna_id
        if antenna_id is None:
            raise ParameterError("antenna id is required")

        if (
            all(
                [
                    name,
                    src,
                    keywords,
                ]
            )
            is False
        ):
            raise ParameterError("Required parameters are missing")
        body = {
            "antennaId": antenna_id,
            "name": name,
            "src": src,
            "userListId": user_list_id,
            "keywords": keywords,
            "excludeKeywords": exclude_keywords,
            "users": users,
            "caseSensitive": case_sensitive,
            "withReplies": with_replies,
            "withFile": with_file,
            "notify": notify,
        }

        res_antenna: IAntenna = await self._session.request(
            Route("POST", "/api/antennas/update"), auth=True, json=body, remove_none=False
        )

        return Antenna(res_antenna, client=self._client)


class AntennaActions(ClientAntennaActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def create(
        self,
        name: str,
        src: IAntennaReceiveSource,
        keywords: list[list[str]],
        exclude_keywords: list[list[str]] | None = None,
        users: list[str] | None = None,
        case_sensitive: bool = False,
        with_replies: bool = False,
        with_file: bool = False,
        notify: bool = False,
        user_list_id: str | None = None,
    ) -> Antenna:
        """Create an antenna.

        Parameters
        ----------
        name : str
            Name of the antenna.
        src : IAntennaReceiveSource
            Receive source of the antenna.
        keywords : list[list[str]]
            Receive keywords.
        exclude_keywords : list[list[str]] | None, default None
            Excluded keywords.
        users : list[str] | None, default None
            List of target user ID. Required when selecting 'users' as the receive source.
        case_sensitive : bool, default False
            Whether to differentiate between uppercase and lowercase letters.
        with_replies : bool, default False
            Whether to include replies.
        with_file : bool, default False
            Whether to limit to notes with attached files.
        notify : bool, default False
            Whether to notify for new notes.
        user_list_id : str | None, default None
            List of user IDs when selecting 'users' as the receive source for the antenna.

        Returns
        -------
        Antenna
            The created antenna.
        """

        if users is None:
            users = [""]
        if exclude_keywords is None:
            exclude_keywords = [[]]

        if (
            all(
                [
                    name,
                    src,
                    keywords,
                ]
            )
            is False
        ):
            raise ParameterError("Required parameters are missing")
        body = {
            "name": name,
            "src": src,
            "userListId": user_list_id,
            "keywords": keywords,
            "excludeKeywords": exclude_keywords,
            "users": users,
            "caseSensitive": case_sensitive,
            "withReplies": with_replies,
            "withFile": with_file,
            "notify": notify,
        }

        res_antenna: IAntenna = await self._session.request(
            Route("POST", "/api/antennas/create"), auth=True, json=body, remove_none=False
        )

        return Antenna(res_antenna, client=self._client)

    async def get_list(self) -> list[Antenna]:
        res_antennas: list[IAntenna] = await self._session.request(
            Route("POST", "/api/antennas/list"), auth=True
        )

        return [Antenna(res_antenna, client=self._client) for res_antenna in res_antennas]
