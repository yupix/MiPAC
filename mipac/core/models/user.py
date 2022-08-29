from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from mipac.types.user import IChannel, IPinnedNote

__all__ = ('RawChannel', 'RawPinnedNote')


class RawChannel:
    def __init__(self, data: IChannel):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if 'created_at' in data else None
        self.last_noted_at: Optional[str] = data.get(
            'last_noted_at'
        )  # TODO: datetimeか確認
        self.name: Optional[str] = data.get('name')
        self.description: Optional[str] = data.get('description')
        self.banner_url: Optional[str] = data.get('banner_url')
        self.notes_count: Optional[int] = data.get('notes_count')
        self.users_count: Optional[int] = data.get('users_count')
        self.is_following: Optional[bool] = data.get('is_following')
        self.user_id: Optional[str] = data.get('user_id')


class RawPinnedNote:
    def __init__(self, data: IPinnedNote):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if 'created_at' in data else None
        self.text: Optional[str] = data.get('text')
        self.cw: Optional[str] = data.get('cw')
        self.user_id: Optional[str] = data.get('user_id')
        self.user: Optional[RawUser] = RawUser(
            data['user']
        ) if 'user' in data else None
        self.reply_id: Optional[str] = data.get('reply_id')
        self.reply: Optional[dict[str, Any]] = data.get('reply')
        self.renote: Optional[dict[str, Any]] = data.get('renote')
        self.via_mobile: bool = data.get('via_mobile', False)
        self.is_hidden: bool = data.get('is_hidden', False)
        self.visibility: bool = bool(
            data['visibility']
        ) if 'visibility' in data else False  # TODO: これ公開範囲?
        self.mentions: Optional[list[str]] = data.get('mentions')
        self.visible_user_ids: Optional[list[str]] = data.get(
            'visible_user_ids'
        )
        self.file_ids: Optional[list[str]] = data.get('file_ids')
        self.files: list[RawFile] = [
            RawFile(i) for i in data['files']
        ] if 'files' in data else []
        self.tags: Optional[list[str]] = data.get('tags')
        self.poll: Optional[dict[str, Any]] = data.get('poll')
        self.channel: Optional[RawChannel] = RawChannel(
            data['channel']
        ) if 'channel' in data else None
        self.local_only: bool = data.get('local_only', False)
        self.emojis: Optional[list[RawEmoji]] = [
            RawEmoji(i) for i in data['emojis']
        ] if 'emojis' in data else None
        self.reactions: Optional[dict[str, Any]] = data.get('reactions')
        self.renote_count: Optional[int] = data.get('renote_count')
        self.replies_count: Optional[int] = data.get('replies_count')
        self.uri: Optional[str] = data.get('uri')
        self.url: Optional[str] = data.get('url')
        self.my_reaction: Optional[dict[str, Any]] = data.get('my_reaction')
