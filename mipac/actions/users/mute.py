from __future__ import annotations

from typing import TYPE_CHECKING, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.mute import Muting
from mipac.types.mute import IMuting
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.client import ClientManager


class SharedMuteActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def create(self, expires_at: int | None = None, *, user_id: str) -> bool:
        """指定したユーザーをミュートします

        Parameters
        ----------
        user_id : str | None
            対象のユーザーID, default=None
        expires_at : int | None
            ミュートする期間(秒)、無期限でミュートする場合はNoneを指定します

        Returns
        -------
        bool
            ミュートに成功したかどうか
        """
        body = {"userId": user_id, "expiresAt": expires_at}

        res: bool = await self._session.request(route=Route("POST", "/api/mute/create"), json=body)

        return res

    async def delete(self, *, user_id: str) -> bool:
        """指定したユーザーのミュートを解除します

        Parameters
        ----------
        user_id : str | None
            対象のユーザーID, default=None

        Returns
        -------
        bool
            ミュート解除に成功したかどうか
        """
        res: bool = await self._session.request(
            route=Route("POST", "/api/mute/delete"), json={"userId": user_id}
        )

        return res


class ClientMuteActions(SharedMuteActions):
    def __init__(self, user_id: str, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user_id: str = user_id

    @override
    async def create(self, expires_at: int | None = None, *, user_id: str | None = None) -> bool:
        """指定したユーザーをミュートします

        Parameters
        ----------
        user_id : str
            対象のユーザーID
        expires_at : int | None
            ミュートする期間(秒)、無期限でミュートする場合はNoneを指定します

        Returns
        -------
        bool
            ミュートに成功したかどうか
        """
        user_id = user_id or self.__user_id

        return await super().create(expires_at=expires_at, user_id=user_id or self.__user_id)

    @override
    async def delete(self, *, user_id: str | None = None) -> bool:
        """指定したユーザーのミュートを解除します

        Parameters
        ----------
        user_id : str
            対象のユーザーID

        Returns
        -------
        bool
            ミュート解除に成功したかどうか
        """
        user_id = user_id or self.__user_id

        return await super().delete(user_id=user_id or self.__user_id)


class MuteActions(SharedMuteActions):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)

    async def get_list(
        self, limit: int = 30, since_id: str | None = None, until_id: str | None = None
    ) -> list[Muting]:
        """ミュートしているユーザーの一覧を取得します

        Returns
        -------
        list[Muting]
            ミュートしているユーザーの一覧
        """

        body = {"limit": limit, "sinceId": since_id, "untilId": until_id}

        mutes: list[IMuting] = await self._session.request(
            Route("GET", "/api/mute/list"), json=body, auth=True
        )

        return [Muting(raw_mute_user=mute, client=self._client) for mute in mutes]

    async def get_all_list(
        self, limit: int = 30, since_id: str | None = None, until_id: str | None = None
    ):
        """ミュートしている全てのユーザーを取得します

        Parameters
        ----------
        limit : int
            取得するユーザー数, by default 30
        since_id : str | None
            指定したIDより後のミュート中のユーザーを取得します,  default=None
        until_id : str | None
            指定したIDより前のミュート中のユーザーを取得します, default=None

        Returns
        -------
        AsyncGenerator[Muting]
            ミュートしているユーザー
        """
        body = {"limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IMuting](
            self._session, Route("GET", "/api/mute/list"), json=body, auth=True
        )

        while pagination.is_final is False:
            for raw_muted_user in await pagination.next():
                yield Muting(raw_mute_user=raw_muted_user, client=self._client)
