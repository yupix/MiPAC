from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.models.lite.user import LiteUser
from mipac.types.invite import IInviteCode, IPartialInviteCode
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


T = TypeVar("T", bound=IPartialInviteCode)


class PartialInviteCode(Generic[T], AbstractModel):
    def __init__(self, raw_invite_code: T, *, client: ClientManager) -> None:
        self._raw_invite_code: T = raw_invite_code
        self._client = client

    @property
    def code(self) -> str:
        return self._raw_invite_code["code"]


class InviteCode(PartialInviteCode[IInviteCode]):
    def __init__(self, raw_invite_code: IInviteCode, *, client: ClientManager) -> None:
        super().__init__(raw_invite_code=raw_invite_code, client=client)

    @property
    def id(self) -> str:
        return self._raw_invite_code["id"]

    @property
    def expires_at(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_invite_code["expires_at"])
            if self._raw_invite_code["expires_at"]
            else None
        )

    @property
    def created_at(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_invite_code["created_at"])
            if self._raw_invite_code["created_at"]
            else None
        )

    @property
    def created_by(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_invite_code["created_by"])
            if self._raw_invite_code["created_by"]
            else None
        )

    @property
    def used_by(self) -> LiteUser | None:
        return (
            LiteUser(self._raw_invite_code["used_by"], client=self._client)
            if self._raw_invite_code["used_by"]
            else None
        )

    @property
    def used_at(self) -> datetime | None:
        return (
            str_to_datetime(self._raw_invite_code["used_at"])
            if self._raw_invite_code["used_at"]
            else None
        )

    @property
    def used(self) -> bool:
        return self._raw_invite_code["used"]
