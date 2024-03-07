from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.hashtag import Hashtag, TrendHashtag
from mipac.models.user import MeDetailed, UserDetailedNotMe, packed_user
from mipac.types.hashtag import IHashtag, ITrendHashtag
from mipac.types.user import IMeDetailedSchema, IUserDetailedNotMeSchema

if TYPE_CHECKING:
    from mipac.client import ClientManager


class HashtagActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def get_list(
        self,
        sort: Literal[
            "+mentionedUsers",
            "-mentionedUsers",
            "+mentionedLocalUsers",
            "-mentionedLocalUsers",
            "+mentionedRemoteUsers",
            "-mentionedRemoteUsers",
            "+attachedUsers",
            "-attachedUsers",
            "+attachedLocalUsers",
            "-attachedLocalUsers",
            "+attachedRemoteUsers",
            "-attachedRemoteUsers",
        ],
        limit: int = 10,
        attached_to_user_only: bool = False,
        attached_to_local_user_only: bool = False,
        attached_to_remote_user_only: bool = False,
    ) -> list[Hashtag]:
        """ハッシュタグのリストを取得します。

        Parameters
        ----------
        sort: Literal[
            "+mentionedUsers",
            "-mentionedUsers",
            "+mentionedLocalUsers",
            "-mentionedLocalUsers",
            "+mentionedRemoteUsers",
            "-mentionedRemoteUsers",
            "+attachedUsers",
            "-attachedUsers",
            "+attachedLocalUsers",
            "-attachedLocalUsers",
            "+attachedRemoteUsers",
            "-attachedRemoteUsers",
        ]
            ソートの方法を指定します。
        limit: int, optional
            取得するハッシュタグの数を指定します, default=10
        attached_to_user_only: bool, optional
            ユーザーに添付されたハッシュタグのみを取得するかどうかを指定します, default=False
        attached_to_local_user_only: bool, optional
            ローカルユーザーに添付されたハッシュタグのみを取得するかどうかを指定します, default=False
        attached_to_remote_user_only: bool, optional
            リモートユーザーに添付されたハッシュタグのみを取得するかどうかを指定します, default=False

        Returns
        -------
        list[Hashtag]
            取得したハッシュタグのリストです。
        """
        body = {
            "limit": limit,
            "attachedToUserOnly": attached_to_user_only,
            "attachedToLocalUserOnly": attached_to_local_user_only,
            "attachedToRemoteUserOnly": attached_to_remote_user_only,
            "sort": sort,
        }

        raw_hashtags: list[IHashtag] = await self.__session.request(
            Route("POST", "/api/hashtags/list"), json=body
        )

        return [
            Hashtag(raw_hashtag=raw_hashtag, client=self.__client) for raw_hashtag in raw_hashtags
        ]

    async def search(self, query: str, limit: int = 10, offset: int = 0) -> list[str]:
        """ハッシュタグを検索します

        Parameters
        ----------
        query: str
            検索するクエリを指定します。
        limit: int, optional
            取得するハッシュタグの数を指定します, default=10
        offset: int, optional
            オフセットを指定します, default=0

        Returns
        -------
        list[Hashtag]
            取得したハッシュタグのリストです。
        """

        body = {"query": query, "limit": limit, "offset": offset}

        raw_hashtags: list[str] = await self.__session.request(
            Route("POST", "/api/hashtags/search"),
            json=body,
            lower=False,  # 戻り値がarrayのstrなのでlowerするとエラーになる
        )

        return raw_hashtags

    async def show(self, tag: str):
        """ハッシュタグの情報を取得します。

        Parameters
        ----------
        tag: str
            取得するハッシュタグの名前です。

        Returns
        -------
        Hashtag
            取得したハッシュタグの情報です。
        """
        body = {"tag": tag}

        raw_hashtag: IHashtag = await self.__session.request(
            Route("POST", "/api/hashtags/show"), json=body
        )

        return Hashtag(raw_hashtag=raw_hashtag, client=self.__client)

    async def get_trend(self):
        """トレンドのハッシュタグを取得します。

        Returns
        -------
        list[TrendHashtag]
            取得したハッシュタグのリストです。
        """
        raw_trend_hashtags: list[ITrendHashtag] = await self.__session.request(
            Route("GET", "/api/hashtags/trend")
        )

        return [
            TrendHashtag(raw_trend_hashtag=raw_trend_hashtag, client=self.__client)
            for raw_trend_hashtag in raw_trend_hashtags
        ]

    async def get_users(
        self,
        tag: str,
        sort: Literal[
            "+follower", "-follower", "+createdAt", "-createdAt", "+updatedAt", "-updatedAt"
        ],
        state: Literal["all", "alive"] = "all",
        origin: Literal["combined", "local", "remote"] = "local",
    ) -> list[UserDetailedNotMe | MeDetailed]:
        body = {"tag": tag, "sort": sort, "state": state, "origin": origin}

        raw_users: list[
            IUserDetailedNotMeSchema | IMeDetailedSchema
        ] = await self.__session.request(Route("POST", "/api/hashtags/users"), json=body)

        return [packed_user(raw_user, client=self.__client) for raw_user in raw_users]
