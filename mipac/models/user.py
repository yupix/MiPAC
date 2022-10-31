from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.models.lite.user import LiteUser
from mipac.models.note import Note
from mipac.types.page import IPage
from mipac.types.user import IFollowRequest, IUserDetailed, IUserDetailedField

if TYPE_CHECKING:
    from mipac.actions.user import UserActions
    from mipac.manager.client import ClientActions

__all__ = ('UserDetailed', 'FollowRequest')


class FollowRequest:
    def __init__(self, request: IFollowRequest, *, client: ClientActions):
        self.__request: IFollowRequest = request
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__request['id']

    @property
    def follower(self) -> LiteUser:
        return LiteUser(self.__request['follower'])

    @property
    def followee(self) -> LiteUser:
        return LiteUser(self.__request['followee'])


class UserDetailed(LiteUser):
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
    def ff_visibility(
        self,
    ) -> Literal['public', 'followers', 'private'] | None:
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
