from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.types.poll import ICreatePoll, IPoll, IPollChoice
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager import ClientManager


class MiPoll:
    def __init__(self, poll: ICreatePoll) -> None:
        self.choices = poll["choices"]
        self.multiple = poll.get("multiple")
        self.expired_after = poll.get("expired_after")
        self.expires_at = poll.get("expires_at")


class PollChoice:
    def __init__(self, choice: IPollChoice, *, client: ClientManager):
        self.__choice: IPollChoice = choice
        self.__client: ClientManager = client

    @property
    def is_voted(self) -> bool:
        return self.__choice["is_voted"]

    @property
    def text(self) -> str:
        return self.__choice["text"]

    @property
    def votes(self) -> int:
        return self.__choice["votes"]

    def _get(self, key: str) -> Any | None:
        return self.__choice.get(key)


class Poll:
    def __init__(self, poll: IPoll, *, client: ClientManager):
        self.__poll: IPoll = poll
        self.__client: ClientManager = client

    @property
    def expires_at(self) -> datetime:
        return str_to_datetime(self.__poll["expires_at"])

    @property
    def multiple(self) -> bool:
        return self.__poll["multiple"]

    @property
    def choices(self) -> list[PollChoice]:
        return [PollChoice(i, client=self.__client) for i in self.__poll["choices"]]

    def _get(self, key: str) -> Any | None:
        return self.__poll.get(key)
