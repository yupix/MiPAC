from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, Optional, overload

from mipac.errors.base import NotExistRequiredData, ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.clip import Clip
from mipac.models.lite.user import PartialUser
from mipac.models.note import Note
from mipac.models.user import Achievement, MeDetailed, UserDetailedNotMe, packed_user
from mipac.types.clip import IClip
from mipac.types.note import INote
from mipac.types.user import IMeDetailedSchema, IUser, is_partial_user
from mipac.utils.cache import cache
from mipac.utils.format import remove_dict_empty
from mipac.utils.pagination import Pagination
from mipac.utils.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ["UserActions"]


class UserActions:
    def __init__(
        self,
        session: HTTPClient,
        client: ClientManager,
        user: Optional[PartialUser] = None,
    ):
        self.__session: HTTPClient = session
        self.__user: Optional[PartialUser] = user
        self.__client: ClientManager = client

    async def get_notes(
        self,
        user_id: str | None = None,
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
    ) -> list[Note]:  # TODO: since_dataなどを用いたページネーションを今後できるようにする
        if check_multi_arg(user_id, self.__user) is False:
            raise ParameterError("missing required argument: user_id", user_id, self.__user)

        user_id = user_id or self.__user and self.__user.id
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

        raw_note: list[INote] = await self.__session.request(
            Route("POST", "/api/users/notes"), json=data
        )

        return [Note(raw_note=raw_note, client=self.__client) for raw_note in raw_note]

    async def get_all_notes(
        self,
        user_id: str | None = None,
        with_replies: bool = False,
        with_renotes: bool = True,
        since_id: str | None = None,
        until_id: str | None = None,
        since_data: int | None = None,
        until_data: int | None = None,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: list[str] | None = None,
        exclude_nsfw: bool = False,
    ):
        user_id = user_id or self.__user and self.__user.id
        data = {
            "userId": user_id,
            "withReplies": with_replies,
            "withRenotes": with_renotes,
            "limit": 100,
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
            self.__session, Route("POST", "/api/users/notes"), json=data
        )

        while pagination.is_final is False:
            res_notes = await pagination.next()
            for note in res_notes:
                yield Note(note, client=self.__client)

    async def get_me(self) -> MeDetailed:  # TODO: トークンが無い場合は例外返すようにする
        """
        ログインしているユーザーの情報を取得します
        """

        res: IMeDetailedSchema = await self.__session.request(
            Route("POST", "/api/i"),
            auth=True,
            lower=True,
        )
        return MeDetailed(res, client=self.__client)

    def get_profile_link(
        self,
        external: bool = True,
        protocol: Literal["http", "https"] = "https",
    ):  # TODO: これモデルに移すべきな気がする
        if not self.__user:
            return None
        host = (
            f"{protocol}://{self.__user.host}"
            if external and self.__user.host
            else self.__session._url
        )
        path = (
            f"/@{self.__user.username}" if external else f"/{self.__user.api.action.get_mention()}"
        )
        return host + path

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
        data: IUser = await self.__session.request(
            Route("POST", "/api/users/show"), json=field, auth=True, lower=True
        )
        return packed_user(data, client=self.__client)

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

    def get_mention(self, user: Optional[PartialUser] = None) -> str:  # TODO: モデルに移す
        """
        Get mention name of user.

        Parameters
        ----------
        user : Optional[User], default=None
            The object of the user whose mentions you want to retrieve

        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData("Required parameters: user")
        return f"@{user.username}@{user.host}" if user.instance else f"@{user.username}"

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
            raise ParameterError("limit は100以下である必要があります")

        if get_all:
            limit = 100

        body = remove_dict_empty(
            {"query": query, "limit": limit, "offset": offset, "origin": origin, "detail": detail}
        )

        pagination = Pagination[IUser](
            self.__session,
            Route("POST", "/api/users/search"),
            json=body,
            pagination_type="count",
        )

        while True:
            users: list[IUser] = await pagination.next()
            for user in users:
                yield (
                    packed_user(user, client=self.__client)
                    if is_partial_user(user) is False
                    else PartialUser(user, client=self.__client)
                )
            if get_all is False or pagination.is_final:
                break

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
            raise ParameterError("limit は100以下である必要があります")

        body = remove_dict_empty(
            {"username": username, "host": host, "limit": limit, "detail": detail}
        )
        res = await self.__session.request(
            Route("POST", "/api/users/search-by-username-and-host"),
            lower=True,
            auth=True,
            json=body,
        )
        return [
            packed_user(user, client=self.__client)
            if detail
            else PartialUser(user, client=self.__client)
            for user in res
        ]

    async def get_achievements(self, user_id: str | None = None) -> list[Achievement]:
        """Get achievements of user."""
        user_id = user_id or self.__user and self.__user.id

        if not user_id:
            raise ParameterError("user_id is required")

        data = {
            "userId": user_id,
        }
        res = await self.__session.request(
            Route("POST", "/api/users/achievements"),
            json=data,
            auth=True,
            lower=True,
        )
        return [Achievement(i) for i in res]

    async def get_clips(
        self,
        user_id: str | None = None,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ):
        user_id = user_id or self.__user and self.__user.id

        if not user_id:
            raise ParameterError("user_id is required")

        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {"userId": user_id, "limit": limit, "sinceId": since_id, "untilId": until_id}

        pagination = Pagination[IClip](
            self.__session, Route("POST", "/api/users/clips"), json=body, auth=True
        )

        while True:
            clips: list[IClip] = await pagination.next()
            for clip in clips:
                yield Clip(clip, client=self.__client)
            if get_all is False or pagination.is_final:
                break
