from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.abstract.model import AbstractModel
from mipac.types.antenna import IAntenna, IAntennaReceiveSource
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.antenna import ClientAntennaManager
    from mipac.manager.client import ClientManager


class Antenna(AbstractModel):
    def __init__(self, antenna: IAntenna, *, client: ClientManager) -> None:
        self.__antenna: IAntenna = antenna
        self.__client: ClientManager = client

    @property
    def case_sensitive(self) -> bool:
        return self.__antenna["case_sensitive"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__antenna["created_at"])

    @property
    def exclude_keywords(self) -> list[str]:
        return self.__antenna["exclude_keywords"]

    @property
    def has_unread_note(self) -> bool:
        return self.__antenna["has_unread_note"]

    @property
    def id(self) -> str:
        return self.__antenna["id"]

    @property
    def is_actor(self) -> bool:
        return self.__antenna["is_actor"]

    @property
    def keywords(self) -> list[str]:
        return self.__antenna["keywords"]

    @property
    def name(self) -> str:
        return self.__antenna["name"]

    @property
    def notify(self) -> bool:
        return self.__antenna["notify"]

    @property
    def src(self) -> IAntennaReceiveSource:
        return self.__antenna["src"]

    @property
    def user_list_id(self) -> str | None:
        return self.__antenna["user_list_id"]

    @property
    def users(self) -> list[str]:
        return self.__antenna["users"]

    @property
    def with_file(self) -> bool:
        return self.__antenna["with_file"]

    @property
    def with_replies(self) -> bool:
        return self.__antenna["with_replies"]

    @property
    def api(self) -> ClientAntennaManager:
        return self.__client.antenna._create_client_antenna_manager(antenna_id=self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Antenna) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
