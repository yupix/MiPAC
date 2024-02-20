from typing import NotRequired, TypedDict

__all__ = ("IPoll", "IPollChoice", "ICreatePoll")


class IPollChoice(TypedDict):
    is_voted: bool
    text: str
    votes: int


class IPoll(TypedDict):
    """
    Questionnaire object
    """

    expires_at: str
    multiple: bool
    choices: list[IPollChoice]


class ICreatePoll(TypedDict):
    choices: list[str]
    multiple: NotRequired[bool]
    expires_at: NotRequired[int]
    expired_after: NotRequired[int]
