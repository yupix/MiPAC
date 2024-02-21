from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, overload, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.clip import Clip
from mipac.models.gallery import GalleryPost
from mipac.models.lite.user import PartialUser
from mipac.models.note import Note
from mipac.models.user import (
    Achievement,
    Follower,
    Following,
    FrequentlyRepliedUser,
    MeDetailed,
    UserDetailedNotMe,
    packed_user,
)
from mipac.types.clip import IClip
from mipac.types.follow import IFederationFollower, IFederationFollowing
from mipac.types.gallery import IGalleryPost
from mipac.types.note import INote
from mipac.types.user import (
    GetFrequentlyRepliedUsersResponse,
    IMeDetailedSchema,
    IUser,
    is_partial_user,
)
from mipac.utils.cache import cache
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination
from mipac.utils.util import deprecated

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ["UserActions"]


class SharedUserActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager) -> None:
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def get_notes(
        self,
        with_replies: bool = False,
        with_renotes: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: list[str] | None = None,
        exclude_nsfw: bool = False,
        *,
        user_id: str,
    ) -> list[Note]:  # TODO: since_dataなどを用いたページネーションを今後できるようにする
        data = {
            "userId": user_id,
            "withReplies": with_replies,
            "withRenotes": with_renotes,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_data,
            "untilDate": until_data,
            "includeMyRenotes": include_my_renotes,
            "withFiles": with_files,
            "fileType": file_type,
            "excludeNsfw": exclude_nsfw,
        }

        raw_note: list[INote] = await self._session.request(
            Route("POST", "/api/users/notes"), json=data, auth=True
        )

        return [Note(raw_note=raw_note, client=self._client) for raw_note in raw_note]

    async def get_all_notes(
        self,
        with_replies: bool = False,
        with_renotes: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: list[str] | None = None,
        exclude_nsfw: bool = False,
        *,
        user_id: str,
    ) -> AsyncGenerator[Note, None]:
        data = {
            "userId": user_id,
            "withReplies": with_replies,
            "withRenotes": with_renotes,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
            "sinceDate": since_data,
            "untilDate": until_data,
            "includeMyRenotes": include_my_renotes,
            "withFiles": with_files,
            "fileType": file_type,
            "excludeNsfw": exclude_nsfw,
        }
        pagination = Pagination[INote](
            self._session, Route("POST", "/api/users/notes"), json=data, auth=True
        )

        while pagination.is_final is False:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self._client)

    async def get_clips(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str,
    ) -> list[Clip]:
        data = {"userId": user_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        raw_clip: list[IClip] = await self._session.request(
            Route("POST", "/api/users/clips"), json=data, auth=True
        )

        return [Clip(raw_clip=raw_clip, client=self._client) for raw_clip in raw_clip]

    async def get_all_clips(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        user_id: str,
    ) -> AsyncGenerator[Clip, None]:
        data = {"userId": user_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IClip](
            self._session, Route("POST", "/api/users/clips"), json=data, auth=True
        )

        while pagination.is_final is False:
            clips: list[IClip] = await pagination.next()
            for clip in clips:
                yield Clip(raw_clip=clip, client=self._client)

    async def get_followers(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        *,
        user_id: str,
    ) -> list[Follower]:
        """
        Get followers of user.

        Endpoint: `/api/users/followers`

        Parameters
        ----------
        since_id : str, default=None
            Get followers after this id.
        until_id : str, default=None
            Get followers before this id.
        limit : int, default=10
            The maximum number of followers to return.
        username : str, default=None
            Get followers with this username.
        host : str, default=None
            Get followers with this host.
        user_id : str, default=None
            Get followers with this user id.

        Returns
        -------
        list[Follower]
            A list of followers.
        """
        data = {
            "userId": user_id,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "username": username,
            "host": host,
        }
        raw_followers: list[IFederationFollower] = await self._session.request(
            Route("POST", "/api/users/followers"), json=data, auth=True
        )

        return [Follower(raw_follower, client=self._client) for raw_follower in raw_followers]

    async def get_all_followers(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        *,
        user_id: str,
    ) -> AsyncGenerator[Follower, None]:
        data = {
            "userId": user_id,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "username": username,
            "host": host,
        }
        pagination = Pagination[IFederationFollower](
            self._session, Route("POST", "/api/users/followers"), json=data, auth=True
        )

        while pagination.is_final is False:
            raw_followers: list[IFederationFollower] = await pagination.next()
            for raw_follower in raw_followers:
                yield Follower(raw_follower, client=self._client)

    async def get_following(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        birthday: str | None = None,
        *,
        user_id: str,
    ) -> list[Following]:
        """Get following of user.

        Endpoint: `/api/users/following`

        Parameters
        ----------
        since_id : str, default=None
            Get following after this id.
        until_id : str, default=None
            Get following before this id.
        limit : int, default=10
            The maximum number of following to return.
        username : str, default=None
            Get following with this username.
        host : str, default=None
            Get following with this host.
        user_id : str, default=None
            Get following with this user id.

        Returns
        -------
        list[Following]
            A list of following.
        """
        data = {
            "userId": user_id,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "username": username,
            "host": host,
            "birthday": birthday,
        }

        raw_following: list[IFederationFollowing] = await self._session.request(
            Route("POST", "/api/users/following"), json=data, auth=True
        )

        return [Following(raw_following, client=self._client) for raw_following in raw_following]

    async def get_all_following(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        birthday: str | None = None,
        *,
        user_id: str,
    ) -> AsyncGenerator[Following, None]:
        data = {
            "userId": user_id,
            "sinceId": since_id,
            "untilId": until_id,
            "limit": limit,
            "username": username,
            "host": host,
            "birthday": birthday,
        }

        pagination = Pagination[IFederationFollowing](
            self._session, Route("POST", "/api/users/following"), json=data, auth=True
        )

        while pagination.is_final is False:
            raw_followings: list[IFederationFollowing] = await pagination.next()
            for raw_following in raw_followings:
                yield Following(raw_following, client=self._client)

    async def get_gallery_posts(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str,
    ) -> list[GalleryPost]:
        """Get gallery posts of user.

        Endpoint: `/api/users/gallery/posts`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of gallery posts to return.
        since_id : str, default=None
            Get gallery posts after this id.
        until_id : str, default=None
            Get gallery posts before this id.
        user_id : str, default=None
            Get gallery posts with this user id.

        Returns
        -------
        list[GalleryPost]
            A list of gallery posts.
        """
        data = {
            "userId": user_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        raw_gallery_posts: list[IGalleryPost] = await self._session.request(
            Route("POST", "/api/users/gallery/posts"), json=data, auth=True
        )

        return [
            GalleryPost(raw_gallery=raw_gallery, client=self._client)
            for raw_gallery in raw_gallery_posts
        ]

    async def get_all_gallery_posts(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str,
    ) -> AsyncGenerator[GalleryPost, None]:
        data = {
            "userId": user_id,
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        pagination = Pagination[IGalleryPost](
            self._session, Route("POST", "/api/users/gallery/posts"), json=data, auth=True
        )

        while pagination.is_final is False:
            raw_gallery_posts: list[IGalleryPost] = await pagination.next()
            for raw_gallery_post in raw_gallery_posts:
                yield GalleryPost(raw_gallery=raw_gallery_post, client=self._client)

    async def get_frequently_replied_users(
        self, limit: int = 10, *, user_id: str
    ) -> list[FrequentlyRepliedUser]:
        """Get frequently replied users of user.

        Endpoint: `/api/users/get-frequently-replied-users`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of frequently replied users to return.
        user_id : str, default=None
            Get frequently replied users with this user id.

        Returns
        -------
        list[FrequentlyRepliedUser]
            A list of frequently replied users.
        """
        data = {
            "userId": user_id,
            "limit": limit,
        }

        res: list[GetFrequentlyRepliedUsersResponse] = await self._session.request(
            Route("POST", "/api/users/get-frequently-replied-users"),
            json=data,
            auth=True,
            lower=True,
        )
        return [FrequentlyRepliedUser(i, client=self._client) for i in res]

    async def get_featured_notes(
        self, limit: int = 10, until_id: str | None = None, *, user_id: str
    ) -> list[Note]:
        """Get featured notes of user.

        Endpoint: `/api/users/featured-notes`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of featured notes to return.
        until_id : str, default=None
            Get featured notes before this id.
        user_id : str, default=None
            Get featured notes with this user id.

        Returns
        -------
        list[Note]
            A list of featured notes.
        """
        data = {
            "userId": user_id,
            "limit": limit,
            "untilId": until_id,
        }

        raw_notes: list[INote] = await self._session.request(
            Route("POST", "/api/users/featured-notes"),
            json=data,
            auth=True,
            lower=True,
        )
        return [Note(raw_note=raw_note, client=self._client) for raw_note in raw_notes]

    async def get_all_featured_notes(
        self, limit: int = 10, until_id: str | None = None, *, user_id: str
    ) -> AsyncGenerator[Note, None]:
        """Get all featured notes of user.

        Endpoint: `/api/users/featured-notes`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of featured notes to return.
        until_id : str, default=None
            Get featured notes before this id.
        user_id : str, default=None
            Get featured notes with this user id.

        Returns
        -------
        list[Note]
            A list of featured notes.
        """
        data = {
            "userId": user_id,
            "limit": limit,
            "untilId": until_id,
        }

        pagination = Pagination[INote](
            self._session, Route("POST", "/api/users/featured-notes"), json=data, auth=True
        )

        while pagination.is_final is False:
            raw_notes: list[INote] = await pagination.next()
            for raw_note in raw_notes:
                yield Note(raw_note=raw_note, client=self._client)

    async def get_achievements(self, *, user_id: str) -> list[Achievement]:
        """Get achievements of user."""
        data = {
            "userId": user_id,
        }
        res = await self._session.request(
            Route("POST", "/api/users/achievements"),
            json=data,
            auth=True,
            lower=True,
        )
        return [Achievement(i) for i in res]


class ClientUserActions(SharedUserActions):
    def __init__(self, user: PartialUser, *, session: HTTPClient, client: ClientManager):
        super().__init__(session=session, client=client)
        self.__user: PartialUser = user

    @override
    async def get_notes(
        self,
        with_replies: bool = False,
        with_renotes: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: list[str] | None = None,
        exclude_nsfw: bool = False,
        *,
        user_id: str | None = None,
    ) -> list[Note]:  # TODO: since_dataなどを用いたページネーションを今後できるようにする
        user_id = user_id or self.__user.id

        return await super().get_notes(
            with_replies=with_replies,
            with_renotes=with_renotes,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_data=since_data,
            until_data=until_data,
            include_my_renotes=include_my_renotes,
            with_files=with_files,
            file_type=file_type,
            exclude_nsfw=exclude_nsfw,
            user_id=user_id,
        )

    @override
    async def get_all_notes(
        self,
        with_replies: bool = False,
        with_renotes: bool = True,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: list[str] | None = None,
        exclude_nsfw: bool = False,
        *,
        user_id: str | None = None,
    ) -> AsyncGenerator[Note, None]:
        user_id = user_id or self.__user.id

        async for i in super().get_all_notes(
            with_replies=with_replies,
            with_renotes=with_renotes,
            limit=limit,
            since_id=since_id,
            until_id=until_id,
            since_data=since_data,
            until_data=until_data,
            include_my_renotes=include_my_renotes,
            with_files=with_files,
            file_type=file_type,
            exclude_nsfw=exclude_nsfw,
            user_id=user_id,
        ):
            yield i

    @override
    async def get_clips(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[Clip]:
        user_id = user_id or self.__user.id

        return await super().get_clips(
            user_id=user_id, limit=limit, since_id=since_id, until_id=until_id
        )

    @override
    async def get_all_clips(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        *,
        user_id: str | None = None,
    ) -> AsyncGenerator[Clip, None]:
        user_id = user_id or self.__user.id

        async for i in super().get_all_clips(
            user_id=user_id, since_id=since_id, limit=limit, until_id=until_id
        ):
            yield i

    @override
    async def get_followers(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[Follower]:
        """
        Get followers of user.

        Endpoint: `/api/users/followers`

        Parameters
        ----------
        since_id : str, default=None
            Get followers after this id.
        until_id : str, default=None
            Get followers before this id.
        limit : int, default=10
            The maximum number of followers to return.
        username : str, default=None
            Get followers with this username.
        host : str, default=None
            Get followers with this host.
        user_id : str, default=None
            Get followers with this user id.

        Returns
        -------
        list[Follower]
            A list of followers.
        """
        user_id = user_id or self.__user.id

        return await super().get_followers(
            since_id=since_id,
            until_id=until_id,
            limit=limit,
            username=username,
            host=host,
            user_id=user_id,
        )

    @override
    async def get_all_followers(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        *,
        user_id: str | None = None,
    ) -> AsyncGenerator[Follower, None]:
        user_id = user_id or self.__user.id

        async for i in super().get_all_followers(
            since_id=since_id,
            until_id=until_id,
            limit=limit,
            username=username,
            host=host,
            user_id=user_id,
        ):
            yield i

    @override
    async def get_following(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        birthday: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[Following]:
        """Get following of user.

        Endpoint: `/api/users/following`

        Parameters
        ----------
        since_id : str, default=None
            Get following after this id.
        until_id : str, default=None
            Get following before this id.
        limit : int, default=10
            The maximum number of following to return.
        username : str, default=None
            Get following with this username.
        host : str, default=None
            Get following with this host.
        user_id : str, default=None
            Get following with this user id.

        Returns
        -------
        list[Following]
            A list of following.
        """
        user_id = user_id or self.__user.id

        return await super().get_following(
            since_id=since_id,
            until_id=until_id,
            limit=limit,
            username=username,
            host=host,
            birthday=birthday,
            user_id=user_id,
        )

    @override
    async def get_all_following(
        self,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        username: str | None = None,
        host: str | None = None,
        birthday: str | None = None,
        *,
        user_id: str | None = None,
    ) -> AsyncGenerator[Following, None]:
        user_id = user_id or self.__user.id

        async for i in super().get_all_following(
            since_id=since_id,
            until_id=until_id,
            limit=limit,
            username=username,
            host=host,
            birthday=birthday,
            user_id=user_id,
        ):
            yield i

    @override
    async def get_gallery_posts(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str | None = None,
    ) -> list[GalleryPost]:
        """Get gallery posts of user.

        Endpoint: `/api/users/gallery/posts`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of gallery posts to return.
        since_id : str, default=None
            Get gallery posts after this id.
        until_id : str, default=None
            Get gallery posts before this id.
        user_id : str, default=None
            Get gallery posts with this user id.

        Returns
        -------
        list[GalleryPost]
            A list of gallery posts.
        """
        user_id = user_id or self.__user.id

        return await super().get_gallery_posts(
            user_id=user_id, limit=limit, since_id=since_id, until_id=until_id
        )

    @override
    async def get_all_gallery_posts(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        *,
        user_id: str | None = None,
    ) -> AsyncGenerator[GalleryPost, None]:
        user_id = user_id or self.__user.id

        async for i in super().get_all_gallery_posts(
            user_id=user_id, limit=limit, since_id=since_id, until_id=until_id
        ):
            yield i

    @override
    async def get_frequently_replied_users(
        self, limit: int = 10, *, user_id: str | None = None
    ) -> list[FrequentlyRepliedUser]:
        """Get frequently replied users of user.

        Endpoint: `/api/users/get-frequently-replied-users`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of frequently replied users to return.
        user_id : str, default=None
            Get frequently replied users with this user id.

        Returns
        -------
        list[FrequentlyRepliedUser]
            A list of frequently replied users.
        """
        user_id = user_id or self.__user.id

        return await super().get_frequently_replied_users(user_id=user_id)

    async def get_featured_notes(
        self, limit: int = 10, until_id: str | None = None, *, user_id: str | None = None
    ) -> list[Note]:
        """Get featured notes of user.

        Endpoint: `/api/users/featured-notes`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of featured notes to return.
        until_id : str, default=None
            Get featured notes before this id.
        user_id : str, default=None
            Get featured notes with this user id.

        Returns
        -------
        list[Note]
            A list of featured notes.
        """
        user_id = user_id or self.__user.id

        return await super().get_featured_notes(user_id=user_id, limit=limit, until_id=until_id)

    async def get_all_featured_notes(
        self, limit: int = 10, until_id: str | None = None, *, user_id: str | None = None
    ) -> AsyncGenerator[Note, None]:
        """Get all featured notes of user.

        Endpoint: `/api/users/featured-notes`

        Parameters
        ----------
        limit : int, default=10
            The maximum number of featured notes to return.
        until_id : str, default=None
            Get featured notes before this id.
        user_id : str, default=None
            Get featured notes with this user id.

        Returns
        -------
        list[Note]
            A list of featured notes.
        """
        user_id = user_id or self.__user.id

        async for i in super().get_all_featured_notes(
            user_id=user_id, limit=limit, until_id=until_id
        ):
            yield i

    async def get_achievements(self, *, user_id: str | None = None) -> list[Achievement]:
        """Get achievements of user."""
        user_id = user_id or self.__user.id

        return await super().get_achievements(user_id=user_id)


class UserActions(SharedUserActions):
    def __init__(
        self,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)

    async def get_me(self) -> MeDetailed:
        """
        ログインしているユーザーの情報を取得します
        """

        res: IMeDetailedSchema = await self._session.request(
            Route("POST", "/api/i"),
            lower=True,
        )
        return MeDetailed(res, client=self._client)

    @cache(group="get_user")
    async def get(
        self,
        user_id: str | None = None,
        user_ids: list[str] | None = None,
        username: str | None = None,
        host: str | None = None,
        **kwargs,
    ) -> UserDetailedNotMe | MeDetailed:
        """
        Retrieve user information from the user ID using the cache.
        If there is no cache, `fetch` is automatically used.
        The `fetch` method is recommended if you want up-to-date user information.

        Parameters
        ----------
        user_id : str
            target user id
        user_ids: list[str]
            target user ids
        username : str
            target username
        host : str, default=None
            Hosts with target users
        """

        field = remove_dict_empty(
            {"userId": user_id, "username": username, "host": host, "userIds": user_ids}
        )
        data: IUser = await self._session.request(
            Route("POST", "/api/users/show"), json=field, auth=True, lower=True
        )
        return packed_user(data, client=self._client)

    async def fetch(
        self,
        user_id: str | None = None,
        user_ids: list[str] | None = None,
        username: str | None = None,
        host: str | None = None,
    ) -> UserDetailedNotMe | MeDetailed:
        """
        Retrieve the latest user information using the target user ID or username.
        If you do not need the latest information, you should basically use the `get` method.
        This method accesses the server each time,
        which may increase the number of server accesses.

        Parameters
        ----------
        user_id : str
            target user id
        username : str
            target username
        username : str
            target username
        host : str, default=None
            Hosts with target users
        """
        return await self.get(
            user_id=user_id, username=username, host=host, user_ids=user_ids, cache_override=True
        )

    @deprecated
    def get_mention(self, user: PartialUser) -> str:
        """対象のユーザーのメンションを取得します

        .. deprecated:: 0.6.3
            :meth:`mipac.models.user.PartialUser._get_mention` を使用することを推奨します。

        Parameters
        ----------
        user : PartialUser
            対象のユーザー

        Returns
        -------
        str
            メンション
        """
        return f"@{user.username}@{user.host}" if user.instance else f"@{user.username}"

    async def search_by_username_and_host(
        self,
        username: str,
        host: str,
        limit: int = 100,
        detail: bool = True,
    ) -> list[UserDetailedNotMe | MeDetailed | PartialUser]:  # TODO: 続き
        """
        Search users by username and host.

        Parameters
        ----------
        username : str
            Username of user.
        host : str
            Host of user.
        limit : int, default=100
            The maximum number of users to return.
        detail : bool, default=True
            Weather to get detailed user information.

        Returns
        -------
        list[UserDetailedNotMe | MeDetailed | PartialUser]
            A list of users.
        """

        if limit > 100:
            raise ValueError("limit は100以下である必要があります")

        body = remove_dict_empty(
            {"username": username, "host": host, "limit": limit, "detail": detail}
        )
        res = await self._session.request(
            Route("POST", "/api/users/search-by-username-and-host"),
            lower=True,
            auth=True,
            json=body,
        )
        return [
            packed_user(user, client=self._client)
            if detail
            else PartialUser(user, client=self._client)
            for user in res
        ]

    @overload
    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[False] = ...,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[PartialUser, None]:
        ...

    @overload
    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[True] = True,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[UserDetailedNotMe | MeDetailed, None]:
        ...

    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        origin: Literal["local", "remote", "combined"] = "combined",
        detail: Literal[True, False] = True,
        *,
        get_all: bool = False,
    ) -> AsyncGenerator[UserDetailedNotMe | MeDetailed | PartialUser, None]:
        """
        Search users by keyword.

        Parameters
        ----------
        query : str
            Keyword to search.
        limit : int, default=100
            The maximum number of users to return.
        offset : int, default=0
            The number of users to skip.
        origin : Literal['local', 'remote', 'combined'], default='combined'
            The origin of users to search.
        detail : Literal[True, False], default=True
            Whether to return detailed user information.
        get_all : bool, default=False
            Whether to return all users.

        """

        if limit > 100:
            raise ValueError("limit は100以下である必要があります")

        if get_all:
            limit = 100

        body = remove_dict_empty(
            {"query": query, "limit": limit, "offset": offset, "origin": origin, "detail": detail}
        )

        pagination = Pagination[IUser](
            self._session,
            Route("POST", "/api/users/search"),
            json=body,
            pagination_type="count",
        )

        while True:
            users: list[IUser] = await pagination.next()
            for user in users:
                yield (
                    packed_user(user, client=self._client)
                    if is_partial_user(user) is False
                    else PartialUser(user, client=self._client)
                )
            if get_all is False or pagination.is_final:
                break
