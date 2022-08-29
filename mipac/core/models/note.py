from __future__ import annotations

from datetime import datetime
from typing import Optional

from mipac.core.models.poll import RawPoll
from mipac.core.models.user import RawUser
from mipac.types.note import IRenote

__all__ = ('RawRenote',)


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
