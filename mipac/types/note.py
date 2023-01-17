from typing import (
    Any,
    Generic,
    Literal,
    NotRequired,
    Optional,
    TypedDict,
    TypeVar,
)

from .drive import IDriveFile
from .emoji import ICustomEmojiLite
from .poll import IPoll
from .user import ILiteUser

T = TypeVar('T')


class INoteState(TypedDict):
    is_favorited: bool
    is_watching: bool
    is_muted_thread: NotRequired[bool]


class INoteUpdated(TypedDict, Generic[T]):
    type: Literal['noteUpdated']
    body: T


class INoteUpdatedDeleteBody(TypedDict):
    deleted_at: str


class INoteUpdatedDelete(TypedDict):
    id: str
    type: Literal['deleted']
    body: INoteUpdatedDeleteBody


class INoteUpdatedReactionBody(TypedDict):
    reaction: str
    emoji: ICustomEmojiLite
    user_id: str


class INoteUpdatedReaction(TypedDict):
    id: str
    type: Literal['reacted', 'unreacted']
    body: INoteUpdatedReactionBody


class GeoPayload(TypedDict):
    """
    衛星情報
    """

    coordinates: Optional[list[Any]]
    altitude: int | None
    accuracy: int | None
    altitude_accuracy: int | None
    heading: int | None
    speed: int | None


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
    emojis: list[ICustomEmojiLite]


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


class INoteTranslateResult(TypedDict):
    sourceLang: str
    text: str
