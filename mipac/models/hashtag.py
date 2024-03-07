from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.types.hashtag import IHashtag, ITrendHashtag

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Hashtag:
    def __init__(self, *, raw_hashtag: IHashtag, client: ClientManager) -> None:
        self.__client: ClientManager = client
        self.__raw_hashtag: IHashtag = raw_hashtag

    @property
    def tag(self):
        return self.__raw_hashtag["tag"]

    @property
    def mentioned_users_count(self):
        return self.__raw_hashtag["mentioned_users_count"]

    @property
    def mentioned_local_users_count(self):
        return self.__raw_hashtag["mentioned_local_users_count"]

    @property
    def mentioned_remote_users_count(self):
        return self.__raw_hashtag["mentioned_remote_users_count"]

    @property
    def attached_users_count(self):
        return self.__raw_hashtag["attached_users_count"]

    @property
    def attached_local_users_count(self):
        return self.__raw_hashtag["attached_local_users_count"]

    @property
    def attached_remote_users_count(self):
        return self.__raw_hashtag["attached_remote_users_count"]

    def _get(self, key: str) -> Any | None:
        """生のレスポンスデータに直接アクセスすることができます
        Returns
        -------
        Any | None
            生のレスポンスデータ
        """
        return self.__raw_hashtag.get(key)


class TrendHashtag:
    def __init__(self, *, raw_trend_hashtag: ITrendHashtag, client: ClientManager) -> None:
        self.__raw_trend_hashtag: ITrendHashtag = raw_trend_hashtag
        self.__client: ClientManager = client

    @property
    def tag(self):
        """ハッシュタグ

        Returns
        -------
        str
            ハッシュタグ
        """
        return self.__raw_trend_hashtag["tag"]

    @property
    def chart(self):
        """チャート

        Returns
        -------
        list[int]
            チャート
        """
        return self.__raw_trend_hashtag["chart"]

    @property
    def users_count(self):
        """ユーザー数

        Returns
        -------
        int
            ユーザー数
        """
        return self.__raw_trend_hashtag["users_count"]

    def _get(self, key: str) -> Any | None:
        """生のレスポンスデータに直接アクセスすることができます
        Returns
        -------
        Any | None
            生のレスポンスデータ
        """
        return self.__raw_trend_hashtag.get(key)
