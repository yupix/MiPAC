from typing import TypedDict

__all__ = ('IPoll', 'IPollChoice')


class IPollChoice(TypedDict):
    is_voted: bool
    text: str
    votes: int


class IPoll(TypedDict, total=False):
    """
    アンケート情報
    """

    multiple: bool
    expires_at: int
    choices: list[IPollChoice]
