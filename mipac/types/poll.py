from typing import TypedDict

__all__ = ('IPoll', 'IPollChoice', 'ICreatePoll', 'IBasePoll')


class IPollChoice(TypedDict):
    is_voted: bool
    text: str
    votes: int


class IBasePoll(TypedDict, total=False):
    multiple: bool
    expires_at: int
    expired_after: int


class ICreatePoll(IBasePoll, total=False):
    choices: list[str]


class IPoll(IBasePoll):
    """
    アンケート情報
    """

    choices: list[IPollChoice]
