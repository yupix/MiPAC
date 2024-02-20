from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.lite.user import PartialUser
from mipac.types.invite import IInviteCode, IInviteLimit
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.invite import ClientInviteManager


class InviteCode:
    def __init__(self, raw_invite_code: IInviteCode, *, client: ClientManager) -> None:
        self.__raw_invite_code: IInviteCode = raw_invite_code
        self.__client = client

    @property
    def id(self) -> str:
        return self.__raw_invite_code["id"]

    @property
    def code(self) -> str:
        return self.__raw_invite_code["code"]

    @property
    def expires_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__raw_invite_code["expires_at"])
            if self.__raw_invite_code["expires_at"]
            else None
        )

    @property
    def created_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__raw_invite_code["created_at"])
            if self.__raw_invite_code["created_at"]
            else None
        )

    @property
    def created_by(self) -> PartialUser | None:
        return (
            PartialUser(self.__raw_invite_code["created_by"], client=self.__client)
            if self.__raw_invite_code["created_by"]
            else None
        )

    @property
    def used_by(self) -> PartialUser | None:
        return (
            PartialUser(self.__raw_invite_code["used_by"], client=self.__client)
            if self.__raw_invite_code["used_by"]
            else None
        )

    @property
    def used_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__raw_invite_code["used_at"])
            if self.__raw_invite_code["used_at"]
            else None
        )

    @property
    def used(self) -> bool:
        return self.__raw_invite_code["used"]

    @property
    def api(self) -> ClientInviteManager:
        return self.__client._create_client_invite_manager(invite_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self.__raw_invite_code.get(key)


class InviteLimit:
    def __init__(self, raw_invite_limit: IInviteLimit, *, client: ClientManager) -> None:
        self.__raw_invite_limit: IInviteLimit = raw_invite_limit
        self.__client = client

    @property
    def remaining(self) -> int | None:
        return self.__raw_invite_limit["remaining"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_invite_limit.get(key)
