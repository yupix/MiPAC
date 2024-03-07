from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.antenna import Antenna
from mipac.models.note import Note
from mipac.types.antenna import IAntenna, IAntennaReceiveSource
from mipac.types.note import INote
from mipac.utils.format import remove_dict_empty, remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedAntennaActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, antenna_id: str) -> bool:
        """Delete antenna from identifier

        Endpoint: `/api/antennas/delete`

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier

        Returns
        -------
        bool
            success or failure
        """
        body = {"antennaId": antenna_id}
        res: bool = await self._session.request(
            Route("POST", "/api/antennas/delete"), auth=True, json=body
        )
        return res

    async def show(self, *, antenna_id: str) -> Antenna:
        """Show antenna from identifier

        Endpoint: `/api/antennas/show`

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier, by default None

        Returns
        -------
        Antenna
            antenna object
        """
        body = {"antennaId": antenna_id}
        res_antenna: IAntenna = await self._session.request(
            Route("POST", "/api/antennas/show"), auth=True, json=body
        )
        return Antenna(res_antenna, client=self._client)

    async def get_notes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: str | None = None,
        until_date: str | None = None,
        *,
        antenna_id: str,
    ) -> list[Note]:
        """ノートを取得します

        Endpoint: `/api/antennas/notes`

        Parameters
        ----------
        antenna_id : str
            アンテナのID
        limit : int, optional
            一度に取得する件数, by default 10
        since_id : str | None
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None
            指定したIDのノートより前のノートを取得します, default=None
        since_date : str | None
            指定した日付のノートより後のノートを取得します, default=None
        until_date : str | None
            指定した日付のノートより前のノートを取得します, default=None

        Returns
        -------
        list[Note]
            取得したノートのリスト
        """
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

        res: list[INote] = await self._session.request(
            Route("POST", "/api/antennas/notes"), json=body
        )
        return [Note(note, client=self._client) for note in res]

    async def get_all_notes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: str | None = None,
        until_date: str | None = None,
        *,
        antenna_id: str,
    ) -> AsyncGenerator[Note, None]:
        """すべてのノートを取得します

        Endpoint: `/api/antennas/notes`

        Parameters
        ----------
        antenna_id : str
            アンテナのID
        limit : int, optional
            一度に取得する件数, default=10
        since_id : str | None, optional
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None, optional
            指定したIDのノートより前のノートを取得します, default=None
        since_date : str | None, optional
            指定した日付のノートより後のノートを取得します, default=None
        until_date : str | None, optional
            指定した日付のノートより前のノートを取得します, default=None

        Yields
        ------
        Iterator[AsyncGenerator[Note, None]]
            取得したノートのリスト
        """
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

        while pagination.is_final is False:
            res_notes = await pagination.next()
            for res_note in res_notes:
                yield Note(res_note, client=self._client)

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
        *,
        antenna_id: str,
    ) -> Antenna:
        """Update an antenna.

        Endpoint: `/api/antennas/update`

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
            raise ValueError("Required parameters are missing")
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


class ClientAntennaActions(SharedAntennaActions):
    def __init__(self, *, antenna_id: str, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__antenna_id: str = antenna_id

    @override
    async def delete(self, *, antenna_id: str | None = None) -> bool:
        """Delete antenna from identifier

        Endpoint: `/api/antennas/delete`

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier

        Returns
        -------
        bool
            success or failure
        """
        antenna_id = antenna_id or self.__antenna_id

        return await super().delete(antenna_id=antenna_id)

    @override
    async def show(self, *, antenna_id: str | None = None) -> Antenna:
        """Show antenna from identifier

        Endpoint: `/api/antennas/show`

        Parameters
        ----------
        antenna_id : str | None, optional
            target identifier, by default None

        Returns
        -------
        Antenna
            antenna object
        """
        antenna_id = antenna_id or self.__antenna_id

        return await super().show(antenna_id=antenna_id)

    @override
    async def get_notes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: str | None = None,
        until_date: str | None = None,
        *,
        antenna_id: str | None = None,
    ) -> list[Note]:
        """ノートを取得します

        Endpoint: `/api/antennas/notes`

        Parameters
        ----------
        limit : int, optional
            一度に取得する件数, by default 10
        since_id : str | None, optional
            指定したIDのノートより後のノートを取得します, by default None
        until_id : str | None, optional
            指定したIDのノートより前のノートを取得します, by default None
        since_date : str | None, optional
            指定した日付のノートより後のノートを取得します, by default None
        until_date : str | None, optional
            指定した日付のノートより前のノートを取得します, by default None
        antenna_id : str | None, optional
            アンテナのID, by default None

        Returns
        -------
        list[Note]
            取得したノートのリスト
        """
        antenna_id = antenna_id or self.__antenna_id

        return await super().get_notes(
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_date=since_date,
            until_date=until_date,
            antenna_id=antenna_id,
        )

    @override
    async def get_all_notes(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_date: str | None = None,
        until_date: str | None = None,
        *,
        antenna_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        """すべてのノートを取得します

        Endpoint: `/api/antennas/notes`

        Parameters
        ----------
        limit : int, optional
            一度に取得する件数, default=10
        since_id : str | None, optional
            指定したIDのノートより後のノートを取得します, default=None
        until_id : str | None, optional
            指定したIDのノートより前のノートを取得します, default=None
        since_date : str | None, optional
            指定した日付のノートより後のノートを取得します, default=None
        until_date : str | None, optional
            指定した日付のノートより前のノートを取得します, default=None
        antenna_id : str | None, optional
            アンテナのID, default=None

        Yields
        ------
        AsyncGenerator[Note, None]
            取得したノートのリスト
        """
        antenna_id = antenna_id or self.__antenna_id

        async for i in super().get_all_notes(
            limit, since_id, until_id, since_date, until_date, antenna_id=antenna_id
        ):
            yield i

    @override
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
        *,
        antenna_id: str | None = None,
    ) -> Antenna:
        """Update an antenna.

        Endpoint: `/api/antennas/update`

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
        antenna_id = antenna_id or self.__antenna_id

        return await super().update(
            name=name,
            src=src,
            keywords=keywords,
            exclude_keywords=exclude_keywords,
            users=users,
            case_sensitive=case_sensitive,
            with_replies=with_replies,
            with_file=with_file,
            notify=notify,
            user_list_id=user_list_id,
            antenna_id=antenna_id,
        )


class AntennaActions(SharedAntennaActions):
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
        local_only: bool = MISSING,
        with_replies: bool = False,
        with_file: bool = False,
        notify: bool = False,
        user_list_id: str | None = None,
    ) -> Antenna:
        """Create an antenna.

        Endpoint: `/api/antennas/create`

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
        local_only : bool, default MISSING
            Whether to limit to local notes.
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
            raise ValueError("Required parameters are missing")
        body = remove_dict_missing(
            {
                "name": name,
                "src": src,
                "userListId": user_list_id,
                "keywords": keywords,
                "excludeKeywords": exclude_keywords,
                "users": users,
                "caseSensitive": case_sensitive,
                "localOnly": local_only,
                "withReplies": with_replies,
                "withFile": with_file,
                "notify": notify,
            }
        )

        res_antenna: IAntenna = await self._session.request(
            Route("POST", "/api/antennas/create"), auth=True, json=body, remove_none=False
        )

        return Antenna(res_antenna, client=self._client)

    async def get_list(self) -> list[Antenna]:
        """アンテナの一覧を取得します

        Endpoint: `/api/antennas/list`

        Returns
        -------
        list[Antenna]
            アンテナのリスト
        """
        res_antennas: list[IAntenna] = await self._session.request(
            Route("POST", "/api/antennas/list"), auth=True
        )

        return [Antenna(res_antenna, client=self._client) for res_antenna in res_antennas]
