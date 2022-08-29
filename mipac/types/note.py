from typing import Any, List, Literal, Optional, TypedDict

from .drive import IDriveFile
from .emoji import ICustomEmojiLite
from .user import IUserLite, UserPayload

__all__ = (
    'INoteRequired',
    'INote',
    'GeoPayload',
    'IPoll',
    'IPollCoice',
    'INoteReaction',
    'IRenote',
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


class IPollCoice(TypedDict):
    is_voted: bool
    text: str
    votes: int


class IPoll(TypedDict, total=False):
    """
    アンケート情報
    """

    multiple: bool
    expires_at: int
    choices: list[IPollCoice]


class IRenoteRequired(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: UserPayload
    text: str
    cw: str
    visibility: str
    renote_count: int
    reactions: dict[str, Any]


class IRenote(IRenoteRequired, total=False):
    replies_count: int
    emojis: List
    file_ids: List
    files: List
    reply_id: str
    renote_id: str
    uri: str
    poll: IPoll
    tags: list[str]
    channel_id: str


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


