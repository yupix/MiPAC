from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from mipac.core.models.drive import RawFile
from mipac.core.models.emoji import RawEmoji
from mipac.core.models.instance import RawInstance
from mipac.types.user import IChannel, IPinnedNote, UserPayload

__all__ = ('RawUserDetails', 'RawUser', 'RawChannel', 'RawPinnedNote')


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


class RawUserDetails:
    """
    ユーザー情報だが、一般的に使うか怪しいもの

    Attributes
    ----------
    avatar_blurhash: Optional[str]
        ユーザーのアバターのblurhash
    avatar_color: str
        ユーザーのアバターの色
    lang: str
        ユーザーの言語
    """

    __slots__ = (
        'avatar_blurhash',
        'avatar_color',
        'banner_url',
        'banner_blurhash',
        'banner_color',
        'two_factor_enabled',
        'use_password_less_login',
        'security_keys',
        'has_pending_follow_request_from_you',
        'has_pending_follow_request_to_you',
        'public_reactions',
        'lang',
    )

    def __init__(self, data):
        self.avatar_blurhash: Optional[str] = data.get('avatar_blurhash')
        self.avatar_color: Optional[str] = data.get('avatar_color')
        self.banner_url = data.get('banner_url')
        self.banner_blurhash = data.get('banner_blurhash')
        self.banner_color = data.get('banner_color')
        self.two_factor_enabled = data.get('two_factor_enabled', False)
        self.use_password_less_login = data.get(
            'use_password_less_login', False
        )
        self.security_keys = data.get('security_keys', False)
        self.has_pending_follow_request_from_you = data.get(
            'has_pending_follow_request_from_you', False
        )
        self.has_pending_follow_request_to_you = data.get(
            'has_pending_follow_request_to_you', False
        )
        self.public_reactions = data.get('public_reactions', False)
        self.lang = data.get('lang')


class RawUser:
    """
    id : str
        ユーザーのID
    name : str
        ユーザーの名前
    nickname : Optional[str]
        ユーザーの表示名
    host : Optional[str]
        # TODO: いい感じに
    avatar_url : Optional[str]
        ユーザーのアバターurl
    is_admin : bool
        管理者か否か
    is_bot : bool
        ボットか否か
    is_cat : bool
        ねこか否か
    is_lady : bool
        お嬢様か否か (Ayuskeyのみ)
    emojis : Optional[list[str]]
        # TODO 謎
    url : Optional[str]
        # TODO 謎
    uri : Optional[str]
        # TODO 謎
    created_at : Optional[datetime]
        ユーザーの作成日時
    ff_visibility : str
        # TODO 謎
    is_following : bool
        フォローされてるか否か
    is_follow : bool
        フォローしているか否か
    is_blocking : bool
        ブロックしているか否か
    is_blocked : bool
        ブロックされてるか否か
    is_muted : bool
        ミュートしているか否か
    details : RawUserDetails
        ユーザーの詳細情報
    instance : Optional[RawInstance]
        インスタンスの情報
    """

    __slots__ = (
        'id',
        'name',
        'nickname',
        'host',
        'avatar_url',
        'is_admin',
        'is_moderator',
        'is_bot',
        'is_cat',
        'is_lady',
        'emojis',
        'online_status',
        'url',
        'uri',
        'created_at',
        'updated_at',
        'is_locked',
        'is_silenced',
        'is_suspended',
        'description',
        'location',
        'birthday',
        'fields',
        'followers_count',
        'following_count',
        'notes_count',
        'pinned_note_ids',
        'pinned_notes',
        'pinned_page_id',
        'pinned_page',
        'ff_visibility',
        'is_following',
        'is_follow',
        'is_blocking',
        'is_blocked',
        'is_muted',
        'details',
        'instance',
    )

    def __init__(self, data: UserPayload):
        self.id: str = data['user_id'] if data.get('user_id') else data['id']
        self.name: str = data['username']
        self.nickname: Optional[str] = data.get('name')
        self.host: Optional[str] = data.get('host')
        self.avatar_url: Optional[str] = data.get('avatar_url')
        self.is_admin: bool = bool(data.get('is_admin'))
        self.is_moderator: bool = bool(data.get('is_moderator'))
        self.is_bot: bool = bool(data.get('is_bot'))
        self.is_cat: bool = bool(data.get('is_cat', False))
        self.is_lady: bool = bool(data.get('is_lady', False))
        self.emojis: Optional[list[str]] = data.get('emojis')
        self.online_status = data.get('online_status', None)
        self.url: Optional[str] = data.get('url')
        self.uri: Optional[str] = data.get('uri')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.updated_at = data.get('updated_at')
        self.is_locked = data.get('is_locked', False)
        self.is_silenced = data.get('is_silenced', False)
        self.is_suspended = data.get('is_suspended', False)
        self.description = data.get('description')
        self.location = data.get('location')
        self.birthday = data.get('birthday')
        self.fields = data.get('fields', [])
        self.followers_count = data.get('followers_count', 0)
        self.following_count = data.get('following_count', 0)
        self.notes_count = data.get('notes_count', 0)
        self.pinned_note_ids = data.get('pinned_note_ids', [])
        self.pinned_notes = data.get('pinned_notes', [])
        self.pinned_page_id = data.get('pinned_page_id')
        self.pinned_page = data.get('pinned_page')
        self.ff_visibility: str = data.get('ff_visibility', 'public')
        self.is_following: bool = bool(data.get('is_following', False))
        self.is_follow: bool = bool(data.get('is_follow', False))
        self.is_blocking: bool = bool(data.get('is_blocking', False))
        self.is_blocked: bool = bool(data.get('is_blocked', False))
        self.is_muted: bool = bool(data.get('is_muted', False))
        self.details: RawUserDetails = RawUserDetails(data)
        self.instance: Optional[RawInstance] = RawInstance(
            data['instance']
        ) if data.get('instance') else None
