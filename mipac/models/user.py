from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from mipac.core.models.user import RawChannel, RawPinnedNote, RawUser
from mipac.types.user import FieldContentPayload, PinnedPagePayload

if TYPE_CHECKING:
    from mipac.actions.user import UserActions
    from mipac.manager.client import ClientActions
    from mipac.models.drive import File
    from mipac.models.emoji import Emoji
    from mipac.models.instance import Instance

__all__ = ['User', 'FollowRequest', 'Followee']


class Followee:
    def __init__(self, data, *, client: ClientActions):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.followee_id: str = data['followee_id']
        self.follower_id: str = data['follower_id']
        self.user: User = User(RawUser(data['follower']), client=client)


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
    def user(self) -> Optional[User]:
        return User(self._raw_data.user, client=self._client)

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
        return [
            self._client._modeler.create_file_instance(i)
            for i in self._raw_data.files
        ]

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
    def emojis(self) -> Optional[list[Emoji]]:
        return [self._client._modeler.new_emoji(i) for i in self._raw_data.emojis]

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


class User:
    def __init__(self, raw_user: RawUser, *, client: ClientActions):
        self.__raw_user = raw_user
        self.__client: ClientActions = client

    @property
    def id(self):
        return self.__raw_user.id

    @property
    def name(self):
        return self.__raw_user.name

    @property
    def nickname(self):
        return self.__raw_user.nickname

    @property
    def host(self):
        return self.__raw_user.host

    @property
    def avatar_url(self):
        return self.__raw_user.avatar_url

    @property
    def is_admin(self):
        return self.__raw_user.is_admin

    @property
    def is_moderator(self):
        return self.__raw_user.is_moderator

    @property
    def is_bot(self):
        return self.__raw_user.is_bot

    @property
    def is_cat(self):
        return self.__raw_user.is_cat

    @property
    def is_lady(self):
        return self.__raw_user.is_lady

    @property
    def emojis(self):
        return self.__raw_user.emojis

    @property
    def online_status(self):
        return self.__raw_user.online_status

    @property
    def url(self):
        return self.__raw_user.url

    @property
    def uri(self):
        return self.__raw_user.uri

    @property
    def created_at(self) -> datetime:
        return self.__raw_user.created_at

    @property
    def updated_at(self):
        return self.__raw_user.updated_at

    @property
    def is_locked(self):
        return self.__raw_user.is_locked

    @property
    def is_silenced(self):
        return self.__raw_user.is_silenced

    @property
    def is_suspended(self):
        return self.__raw_user.is_suspended

    @property
    def description(self):
        return self.__raw_user.description

    @property
    def location(self):
        return self.__raw_user.location

    @property
    def birthday(self):
        return self.__raw_user.birthday

    @property
    def fields(self):
        return self.__raw_user.fields

    @property
    def followers_count(self):
        return self.__raw_user.followers_count

    @property
    def following_count(self):
        return self.__raw_user.following_count

    @property
    def notes_count(self):
        return self.__raw_user.notes_count

    @property
    def pinned_note_ids(self):
        return self.__raw_user.pinned_note_ids

    @property
    def pinned_notes(self):
        return self.__raw_user.pinned_notes

    @property
    def pinned_page_id(self):
        return self.__raw_user.pinned_page_id

    @property
    def pinned_page(self):
        return self.__raw_user.pinned_page

    @property
    def ff_visibility(self):
        return self.__raw_user.ff_visibility

    @property
    def is_following(self):
        return self.__raw_user.is_following

    @property
    def is_follow(self):
        return self.__raw_user.is_follow

    @property
    def is_blocking(self):
        return self.__raw_user.is_blocking

    @property
    def is_blocked(self):
        return self.__raw_user.is_blocked

    @property
    def is_muted(self):
        return self.__raw_user.is_muted

    @property
    def details(self):
        return self.__raw_user.details

    @property
    def instance(self) -> Union[Instance, None]:
        return (
            self.__client._modeler.new_instance(self.__raw_user.instance)
            if self.__raw_user.instance
            else None
        )

    @property
    def action(self) -> UserActions:
        return self.__client._create_user_instance(self).action
