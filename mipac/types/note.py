from typing import Any, Generic, Literal, NotRequired, Optional, TypedDict, TypeVar

from mipac.types.drive import IDriveFile
from mipac.types.emoji import ICustomEmojiLite
from mipac.types.poll import IPoll
from mipac.types.reaction import IReactionAcceptance
from mipac.types.user import IPartialUser

T = TypeVar("T")

INoteVisibility = Literal["public", "home", "followers", "specified"]


class INoteState(TypedDict):
    is_favorited: bool
    is_muted_thread: bool


class INoteUpdated(TypedDict, Generic[T]):
    type: Literal["noteUpdated"]
    body: T


class INoteUpdatedDeleteBody(TypedDict):
    deleted_at: str


class INoteUpdatedDelete(TypedDict):
    id: str
    type: Literal["deleted"]
    body: INoteUpdatedDeleteBody


class INoteUpdatedReactionBody(TypedDict):
    reaction: str
    emoji: ICustomEmojiLite
    user_id: str


class INoteUpdatedReaction(TypedDict):
    id: str
    type: Literal["reacted", "unreacted"]
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


class IPartialNote(TypedDict):
    created_at: str
    cw: str | None
    file_ids: list[str]
    files: list[IDriveFile]
    id: str
    reaction_acceptance: NotRequired[IReactionAcceptance]  # v13 only
    reaction_emojis: NotRequired[dict[str, str]]  # v13 only
    renote_id: str | None
    renote_count: int
    reactions: dict[str, int]
    replies_count: int
    reply_id: str | None
    text: str | None
    user: IPartialUser
    user_id: str
    visibility: INoteVisibility
    tags: NotRequired[list[str]]  # タグがついてないとbodyに存在しない


class INote(IPartialNote, total=False):
    """
    note object
    """

    renote: "INote"
    reply: "INote"
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
    user: IPartialUser
    type: str


class INoteTranslateResult(TypedDict):
    sourceLang: str
    text: str
