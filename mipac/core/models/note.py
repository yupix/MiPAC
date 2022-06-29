from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from mipac.core.models.drive import RawFile
from mipac.core.models.emoji import RawEmoji
from mipac.core.models.poll import RawPoll
from mipac.core.models.user import RawUser
from mipac.types.note import INote, IReaction, IRenote
from mipac.util import upper_to_lower

__all__ = ('RawRenote', 'RawReaction', 'RawNote')


class RawRenote:
    """
    Attributes
    ----------
    id : str
    created_at : datetime
    user_id :str
    user : RawUser
    content: Optional[str], default=None
    cw : Optional[str], default=None
    visibility : str
    renote_count : int | None
    replies_count : int | None
    reactions
    emojis
    file_ids : list[str]
    files
    reply_id
    renote_id
    uri
    poll Optional[RawPoll]
    """

    __slots__ = (
        'id',
        'created_at',
        'user_id',
        'user',
        'content',
        'cw',
        'visibility',
        'renote_count',
        'replies_count',
        'replies_count',
        'reactions',
        'emojis',
        'file_ids',
        'files',
        'reply_id',
        'renote_id',
        'uri',
        'poll',
    )

    def __init__(self, data: IRenote):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.user_id: str = data['user_id']
        self.user: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get('text', None)
        self.cw: Optional[str] = data.get('cw')
        self.visibility: str = data['visibility']
        self.renote_count: int | None = data.get('renote_count')
        self.replies_count: int | None = data.get('replies_count')
        self.reactions = data['reactions']  # TODO:型探す
        self.emojis = data.get('emojis')  # TODO:型探す
        self.file_ids: Optional[list[str]] = data.get('file_ids')
        self.files = data.get('files')
        self.reply_id = data.get('reply_id')
        self.renote_id = data.get('renote_id')
        self.uri = data.get('uri')
        self.poll: Optional[RawPoll] = RawPoll(
            data['poll']
        ) if 'poll' in data else None


class RawReaction:
    """
    Attributes
    ----------
    id : Optional[str], default=None
    created_at : Optional[datetime], default=None
    type : Optional[str], default=None
    is_read : bool
    user : Optional[RawUser], default=None
    note : Optional[RawNote], default=None
    reaction : str
    """

    __slots__ = (
        'id',
        'created_at',
        'type',
        'is_read',
        'user',
        'note',
        'reaction',
    )

    def __init__(self, data: IReaction):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if 'created_at' in data else None
        self.type: Optional[str] = data.get('type')
        self.is_read: bool = bool(data.get('is_read'))
        self.user: Optional[RawUser] = RawUser(
            data['user']
        ) if 'user' in data else None
        self.note: Optional[RawNote] = RawNote(
            data['note']
        ) if 'note' in data else None
        self.reaction: str = data['reaction']


class RawNote:
    """
    Attributes
    ----------
    id :  str
    created_at :  datetime
    user_id :  str
    author :  RawUser
    content : Optional[str]
    cw : Optional[str]
    renote : Optional[RawRenote]
    visibility : Optional[str]
    renote_count : Optional[int]
    replies_count : Optional[int]
    reactions : Optional[dict[str, Any]]
    emojis : list[RawEmoji]
    file_ids : Optional[list[str]]
    files : list[RawFile]
    reply_id : Optional[str]
    renote_id : Optional[str]
    poll : Optional[RawPoll]
    visible_user_ids : Optional[list[str]]
    via_mobile :  bool
    local_only :  bool
    extract_mentions :  bool
    extract_hashtags :  bool
    extract_emojis :  bool
    preview :  bool
    media_ids : Optional[list[str]]
    field : Optional[dict]
    tags : Optional[list[str]]
    channel_id : Optional[str]
    """

    __slots__ = (
        'id',
        'created_at',
        'user_id',
        'author',
        'content',
        'cw',
        'renote',
        'visibility',
        'renote_count',
        'replies_count',
        'reactions',
        'emojis',
        'file_ids',
        'files',
        'reply_id',
        'renote_id',
        'uri',
        'poll',
        'visible_user_ids',
        'via_mobile',
        'local_only',
        'extract_mentions',
        'extract_hashtags',
        'extract_emojis',
        'preview',
        'media_ids',
        'field',
        'tags',
        'channel_id',
    )

    def __init__(self, data: INote):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.user_id: str = data['user_id']
        self.author: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get('text')
        self.cw: Optional[str] = data.get('cw')
        self.renote: Optional[RawRenote] = RawRenote(
            data['renote']
        ) if 'renote' in data else None
        self.visibility: Optional[str] = data.get('visibility')
        self.renote_count: Optional[int] = data.get('renote_count')
        self.replies_count: Optional[int] = data.get('replies_count')
        self.reactions: dict[str, Any] = data['reactions']
        self.emojis: list[RawEmoji] = [RawEmoji(i) for i in data['emojis']]
        self.file_ids: Optional[list[str]] = data.get('file_ids')
        self.files: list[RawFile] = [
            RawFile(upper_to_lower(i)) for i in data['files']
        ] if 'files' in data else []
        self.reply_id: Optional[str] = data.get('reply_id')
        self.renote_id: Optional[str] = data.get('renote_id')
        self.poll: Optional[RawPoll] = RawPoll(
            data['poll']
        ) if 'poll' in data else None
        self.visible_user_ids: Optional[list[str]] = data.get(
            'visible_user_ids', []
        )
        self.via_mobile: bool = bool(data.get('via_mobile', False))
        self.local_only: bool = bool(data.get('local_only', False))
        self.extract_mentions: bool = bool(data.get('extract_mentions'))
        self.extract_hashtags: bool = bool(data.get('extract_hashtags'))
        self.extract_emojis: bool = bool(data.get('extract_emojis'))
        self.preview: bool = bool(data.get('preview'))
        self.media_ids: Optional[list[str]] = data.get('media_ids')
        self.field: Optional[dict[Any, Any]] = {}
        self.tags: Optional[list[str]] = data.get('tags', [])
        self.channel_id: Optional[str] = data.get('channel_id')
