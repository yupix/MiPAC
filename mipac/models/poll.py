from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.types.poll import ICreatePoll, IPoll, IPollChoice

if TYPE_CHECKING:
    from mipac.manager import ClientActions


class MiPoll:
    def __init__(self, poll: ICreatePoll) -> None:
        self.multiple = poll.get('multiple', False)
        self.choices = poll.get('choices')
        self.expired_after = poll.get('expired_after')
        self.expires_at = poll.get('expires_at')


class PollChoice:
    def __init__(self, choice: IPollChoice, *, client: ClientActions):
        self.__choice: IPollChoice = choice
        self.__client: ClientActions = client

    @property
    def is_voted(self) -> bool:
        return self.__choice['is_voted']

    @property
    def text(self) -> str:
        return self.__choice['text']

    @property
    def votes(self) -> int:
        return self.__choice['votes']


class Poll:
    def __init__(self, poll: IPoll, *, client: ClientActions):
        self.__poll: IPoll = poll
        self.__client: ClientActions = client

    @property
    def multiple(self) -> bool:
        return self.__poll['multiple']

    @property
    def expires_at(self) -> int:
        return self.__poll['expires_at']

    @property
    def expired_after(self) -> int:
        return self.__poll['expired_after']

    @property
    def choices(self) -> list[PollChoice]:
        return [
            PollChoice(i, client=self.__client) for i in self.__poll['choices']
        ]
