from typing import Any, Literal, Optional, TypedDict

from .drive import IDriveFile
from .emoji import ICustomEmojiLite
from .user import IUserLite

__all__ = (
    'INoteRequired',
    'INote',
    'GeoPayload',
    'IPoll',
    'IPollChoice',
    'INoteReaction',
)


class GeoPayload(TypedDict):
    """
    衛星情報
    """

    coordinates: Optional[list[Any]]
    altitude: Optional[int]
    accuracy: Optional[int]
    altitude_accuracy: Optional[int]
    heading: Optional[int]
    speed: Optional[int]


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


class INoteRequired(TypedDict):
    id: str
    created_at: str
    text: str | None
    cw: str | None
    user: IUserLite
    user_id: str
    reply_id: str
    renote_id: str
    files: list[IDriveFile]
    file_ids: list[str]
    visibility: Literal['public', 'home', 'followers', 'specified']
    reactions: dict[str, int]
    renote_count: int
    replies_count: int
    emojis: list[ICustomEmojiLite]


class INote(INoteRequired, total=False):
    """
    note object
    """

    renote: 'INote'
    reply: 'INote'
    visible_user_ids: list[str]
    local_only: bool
    my_reaction: str
    uri: str
    url: str
    is_hidden: bool
    poll: IPoll


class INoteReaction(TypedDict):
    id: str
    created_at: str
    user: IUserLite
    type: str
