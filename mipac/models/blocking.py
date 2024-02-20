from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.user import UserDetailedNotMe, packed_user
from mipac.types.blocking import IBlocking
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.blocking import ClientBlockingManager
    from mipac.manager.client import ClientManager


class Blocking:
    def __init__(self, *, raw_blocking: IBlocking, client: ClientManager) -> None:
        self.__raw_blocking: IBlocking = raw_blocking
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """ブロックID

        Returns
        -------
        str
            ブロックID
        """
        return self.__raw_blocking["id"]

    @property
    def created_at(self) -> datetime:
        """ブロックした日時

        Returns
        -------
        datetime
            ブロックした日時
        """
        return str_to_datetime(self.__raw_blocking["created_at"])

    @property
    def blockee_id(self) -> str:
        """ブロック対象のユーザーID

        Returns
        -------
        str
            ブロック対象のユーザーID
        """
        return self.__raw_blocking["blockee_id"]

    @property
    def blockee(self) -> UserDetailedNotMe:
        """ブロック対象のユーザー情報

        Returns
        -------
        UserDetailedNotMe
            ブロック対象のユーザー情報
        """
        return packed_user(self.__raw_blocking["blockee"], client=self.__client)

    @property
    def api(self) -> ClientBlockingManager:
        """ブロック対象に対するAPIを利用するためのManager

        Returns
        -------
        ClientBlockingManager
            ブロック対象に対するAPIを利用するためのManager
        """
        return self.__client.user._create_client_blocking_manager(user_id=self.blockee.id)

    def _get(self, key: str) -> Any | None:
        return self.__raw_blocking.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Blocking) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
