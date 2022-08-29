from __future__ import annotations

from datetime import datetime
from typing import Any, List, Literal, Optional, TYPE_CHECKING

from mipac.models.note import Note
from mipac.core.models.user import RawChannel, RawPinnedNote
from mipac.models.emoji import CustomEmoji
from mipac.models.lite.user import UserLite
from mipac.types.page import IPage
from mipac.types.user import (
    FieldContentPayload,
    IUserDetailed,
    IUserDetailedField,
    PinnedPagePayload,
)

if TYPE_CHECKING:
    from mipac.actions.user import UserActions
    from mipac.manager.client import ClientActions
    from mipac.models.drive import File

__all__ = ['UserDetailed', 'FollowRequest', 'Followee']


class Followee:
    def __init__(self, data, *, client: ClientActions):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.followee_id: str = data['followee_id']
        self.follower_id: str = data['follower_id']
        self.user: UserDetailed = UserDetailed(
            RawUser(data['follower']), client=client
        )


class FollowRequest:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['username']
        self.nickname = data['name']
        self.host = data['host']
        self.avatar_url = data['avatar_url']
        self.avatar_blurhash = data['avatar_blurhash']
        self.avatar_color = data['avatar_color']
        self.emojis = data['emojis']
        self.online_status = data['online_status']
        self.is_admin: bool = bool(data.get('is_admin'))
        self.is_bot: bool = bool(data.get('is_bot'))
        self.is_cat: bool = bool(data.get('is_cat'))


class Channel:
    def __init__(self, raw_data: RawChannel, *, client: ClientActions):
        self.__client: ClientActions = client
        self.__raw_data: RawChannel = raw_data

    @property
    def id(self) -> str:
        return self.__raw_data.id

    @property
    def created_at(self) -> Optional[datetime]:
        return self.__raw_data.created_at

    @property
    def last_noted_at(self) -> Optional[str]:
        return self.__raw_data.last_noted_at

    @property
    def name(self) -> Optional[str]:
        return self.__raw_data.name

    @property
    def description(self) -> Optional[str]:
        return self.__raw_data.description

    @property
    def banner_url(self) -> Optional[str]:
        return self.__raw_data.banner_url

    @property
    def notes_count(self) -> Optional[int]:
        return self.__raw_data.notes_count

    @property
    def users_count(self) -> Optional[int]:
        return self.__raw_data.users_count

    @property
    def is_following(self) -> Optional[bool]:
        return self.__raw_data.is_following

    @property
    def user_id(self) -> Optional[str]:
        return self.__raw_data.user_id


class PinnedNote:
    def __init__(self, raw_data: RawPinnedNote, *, client: ClientActions):
        self._client: ClientActions = client
        self._raw_data: RawPinnedNote = raw_data

    @property
    def id(self) -> Optional[str]:
        return self._raw_data.id

    @property
    def created_at(self) -> Optional[datetime]:
        return self._raw_data.created_at

    @property
    def text(self) -> Optional[str]:
        return self._raw_data.text

    @property
    def cw(self) -> Optional[str]:
        return self._raw_data.cw

    @property
    def user_id(self) -> Optional[str]:
        return self._raw_data.user_id

    @property
    def user(self) -> Optional[UserDetailed]:
        return UserDetailed(self._raw_data.user, client=self._client)

    @property
    def reply_id(self) -> Optional[str]:
        return self._raw_data.reply_id

    @property
    def reply(self) -> Optional[dict[str, Any]]:
        return self._raw_data.reply

    @property
    def renote(self) -> Optional[dict[str, Any]]:
        return self._raw_data.renote

    @property
    def via_mobile(self) -> bool:
        return self._raw_data.via_mobile

    @property
    def is_hidden(self) -> bool:
        return self._raw_data.is_hidden

    @property
    def visibility(self) -> bool:
        return self._raw_data.visibility

    @property
    def mentions(self) -> Optional[list[str]]:
        return self._raw_data.mentions

    @property
    def visible_user_ids(self) -> Optional[list[str]]:
        return self._raw_data.visible_user_ids

    @property
    def file_ids(self) -> Optional[list[str]]:
        return self._raw_data.file_ids

    @property
    def files(self) -> list[File]:
        return [File(i, client=self._client) for i in self._raw_data.files]

    @property
    def tags(self) -> Optional[list[str]]:
        return self._raw_data.tags

    @property
    def poll(self) -> Optional[dict[str, Any]]:
        return self._raw_data.poll

    @property
    def channel(self) -> Optional[Channel]:
        return Channel(self._raw_data.channel, client=self._client)

    @property
    def local_only(self) -> bool:
        return self._raw_data.local_only

    @property
    def emojis(self) -> list[CustomEmoji] | None:
        return [
            CustomEmoji(i, client=self._client) for i in self._raw_data.emojis
        ]

    @property
    def reactions(self) -> Optional[dict[str, Any]]:
        return self._raw_data.reactions

    @property
    def renote_count(self) -> Optional[int]:
        return self._raw_data.renote_count

    @property
    def replies_count(self) -> Optional[int]:
        return self._raw_data.replies_count

    @property
    def uri(self) -> Optional[str]:
        return self._raw_data.uri

    @property
    def url(self) -> Optional[str]:
        return self._raw_data.url

    @property
    def my_reaction(self) -> Optional[dict[str, Any]]:
        return self._raw_data.my_reaction


class PinnedPage:
    def __init__(self, data: PinnedPagePayload):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.updated_at: Optional[str] = data.get('updated_at', None)
        self.title: Optional[str] = data.get('title')
        self.name: Optional[str] = data.get('name')
        self.summary: Optional[str] = data.get('summary')
        self.content: Optional[List] = data.get('content')
        self.variables: Optional[List] = data.get('variables')
        self.user_id: Optional[str] = data.get('user_id')
        self.author: Optional[dict[str, Any]] = data.get('author')


class FieldContent:
    def __init__(self, data: FieldContentPayload):
        self.name: str = data['name']
        self.value: str = data['value']


class UserDetailed(UserLite):
    __slots__ = (
        '__detail',
        '__client',
    )

    def __init__(self, user: IUserDetailed, *, client: ClientActions):
        super().__init__(user=user)
        self.__detail = user
        self.__client: ClientActions = client

    @property
    def fields(self) -> list[IUserDetailedField]:
        return self.__detail['fields']

    @property
    def followers_count(self) -> int:
        return self.__detail['followers_count']

    @property
    def following_count(self) -> int:
        return self.__detail['following_count']

    @property
    def has_pending_follow_request_from_you(self) -> bool:
        return self.__detail['has_pending_follow_request_from_you']

    @property
    def has_pending_follow_request_to_you(self) -> bool:
        return self.__detail['has_pending_follow_request_to_you']

    @property
    def is_admin(self) -> bool:
        return self.__detail['is_admin']

    @property
    def is_blocked(self) -> bool:
        return self.__detail['is_blocked']

    @property
    def is_blocking(self) -> bool:
        return self.__detail['is_blocking']

    @property
    def is_bot(self) -> bool:
        return self.__detail['is_bot']

    @property
    def is_cat(self) -> bool:
        return self.__detail['is_cat']

    @property
    def is_followed(self) -> bool:
        return self.__detail['is_followed']

    @property
    def is_following(self) -> bool:
        return self.__detail['is_following']

    @property
    def is_locked(self) -> bool:
        return self.__detail['is_locked']

    @property
    def is_moderator(self) -> bool:
        return self.__detail['is_moderator']

    @property
    def is_muted(self) -> bool:
        return self.__detail['is_muted']

    @property
    def is_silenced(self) -> bool:
        return self.__detail['is_silenced']

    @property
    def is_suspended(self) -> bool:
        return self.__detail['is_suspended']

    @property
    def public_reactions(self) -> bool:
        return self.__detail['public_reactions']

    @property
    def security_keys(self) -> bool:
        return self.__detail['security_keys']

    @property
    def two_factor_enabled(self) -> bool:
        return self.__detail['two_factor_enabled']

    @property
    def notes_count(self) -> int:
        return self.__detail['notes_count']

    @property
    def pinned_note_ids(self) -> list[str]:
        return self.__detail['pinned_note_ids']

    @property
    def pinned_notes(self) -> list[Note]:
        return [
            Note(i, client=self.__client)
            for i in self.__detail['pinned_notes']
        ]

    @property
    def banner_blurhash(self) -> str | None:
        return self.__detail.get('banner_blurhash')

    @property
    def banner_color(self) -> str | None:
        return self.__detail.get('banner_color')

    @property
    def banner_url(self) -> str | None:
        return self.__detail.get('banner_url')

    @property
    def birthday(self) -> str | None:
        return self.__detail.get('birthday')

    @property
    def created_at(self) -> str | None:
        return self.__detail.get('created_at')

    @property
    def description(self) -> str | None:
        return self.__detail.get('description')

    @property
    def ff_visibility(self) -> Literal['public', 'followers', 'private']:
        return self.__detail.get('ff_visibility')

    @property
    def lang(self) -> str | None:
        return self.__detail.get('lang')

    @property
    def last_fetched_at(self) -> str | None:
        return self.__detail.get('last_fetched_at')

    @property
    def location(self) -> str | None:
        return self.__detail.get('location')

    @property
    def pinned_page(self) -> IPage | None:
        return self.__detail.get('pinned_page')

    @property
    def pinned_page_id(self) -> str | None:
        return self.__detail.get('pinned_page_id')

    @property
    def updated_at(self) -> str | None:
        return self.__detail.get('updated_at')

    @property
    def uri(self) -> str | None:
        return self.__detail.get('uri')

    @property
    def url(self) -> str | None:
        return self.__detail.get('url')

    @property
    def action(self) -> UserActions:
        return self.__client._create_user_instance(self).action
