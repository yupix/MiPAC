from typing import Any, Literal, Optional, TypedDict, TypeVar

from .drive import IDriveFile
from .emoji import ICustomEmojiLite
from .poll import IPoll
from .user import ILiteUser

T = TypeVar('T')


class INoteUpdated(TypedDict):
    type: Literal['noteUpdated']
    body: T


class INoteUpdatedReactionBody(TypedDict):
    reaction: str
    emoji: ICustomEmojiLite


class INoteUpdatedReaction(TypedDict):
    id: str
    type: Literal['reacted']
    body: INoteUpdatedReactionBody
    user_id: str


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


class INoteRequired(TypedDict):
    id: str
    created_at: str
    text: str | None
    cw: str | None
    user: ILiteUser
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


class ICreatedNote(TypedDict):
    """
    created note
    """

    created_note: INote


class INoteReaction(TypedDict):
    id: str
    created_at: str
    user: ILiteUser
    type: str
