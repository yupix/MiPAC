from typing import Any, Dict, List, Optional, TypedDict

from .drive import FilePayload
from .emoji import EmojiPayload
from .user import UserPayload

__all__ = (
    'INoteRequired',
    'INote',
    'GeoPayload',
    'ReactionPayload',
    'PollPayload',
    'RenotePayload',
    'OptionalReaction',
)


class GeoPayload(TypedDict):
    """
    衛星情報
    """

    coordinates: Optional[List[Any]]
    altitude: Optional[int]
    accuracy: Optional[int]
    altitude_accuracy: Optional[int]
    heading: Optional[int]
    speed: Optional[int]


class PollPayload(TypedDict, total=False):
    """
    アンケート情報
    """

    multiple: bool
    expires_at: int
    choices: List[str]
    expired_after: int


class RenotePayload(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: UserPayload
    text: str
    cw: str
    visibility: str
    renote_count: int
    replies_count: Optional[int]
    reactions: Dict[str, Any]
    emojis: Optional[List]
    file_ids: Optional[List]
    files: Optional[List]
    reply_id: Optional[str]
    renote_id: Optional[str]
    uri: Optional[str]
    poll: Optional[PollPayload]
    tags: Optional[List[str]]
    channel_id: Optional[str]


class INoteRequired(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: UserPayload
    emojis: List[EmojiPayload]
    reactions: Dict[str, Any]


class INote(INoteRequired, total=False):
    """
    note object
    """
    visibility: str
    renote_count: int
    replies_count: int
    file_ids: List[str]
    files: List[FilePayload]
    reply_id: str
    renote_id: str
    poll: PollPayload
    visible_user_ids: List[str]
    via_mobile: bool
    local_only: bool
    extract_mentions: bool
    extract_hashtags: bool
    extract_emojis: bool
    preview: bool
    media_ids: List[str]
    renote: RenotePayload
    field: dict
    tags: List[str]
    channel_id: str
    text: str
    cw: str
    geo: GeoPayload



class OptionalReaction(TypedDict, total=False):
    created_at: str
    type: str
    is_read: bool
    user: UserPayload
    note: INote
    id: str


class ReactionPayload(OptionalReaction):
    reaction: str
