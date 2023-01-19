from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING

from mipac.models.user import UserDetailed
from mipac.types.admin import IModerationLog
from mipac.util import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class ModerationLog:
    def __init__(self, moderation_log: IModerationLog, *, client: ClientManager) -> None:
        self.__moderation_log: IModerationLog = moderation_log
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__moderation_log['id']

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__moderation_log['created_at'])

    @property
    def type(self) -> str:
        return self.__moderation_log['type']

    @property
    def info(self) -> dict:
        return self.__moderation_log['info']

    @property
    def user_id(self) -> str:
        return self.__moderation_log['user_id']

    @property
    def user(self) -> UserDetailed:
        return UserDetailed(self.__moderation_log['user'], client=self.__client)
