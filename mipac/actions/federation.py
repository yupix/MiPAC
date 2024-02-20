from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.instance import FederationInstance
from mipac.models.user import MeDetailed, UserDetailedNotMe, packed_user
from mipac.types.follow import IFederationFollower, IFederationFollowing
from mipac.types.instance import IFederationInstance, IFederationInstanceStat
from mipac.types.user import IUserDetailed
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class FederationActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_ap(self, uri: str) -> dict[Any, Any]:
        return dict(
            await self.__session.request(
                Route("POST", "/api/ap/get"), auth=True, json={"uri": uri}, lower=True
            )
        )

    async def show_ap(
        self, host: str, since_id: str | None = None, until_id: str | None = None, limit: int = 10
    ) -> FederationInstance:  # TODO: 存在するのか確認する
        body = {"host": host, "sinceId": since_id, "untilId": until_id, "limit": limit}

        res: FederationInstance = await self.__session.request(
            Route("POST", "/api/ap/show"), auth=True, json=body
        )
        return res

    async def get_followers(
        self,
        host: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        get_all: bool = False,
    ):
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")

        if get_all:
            limit = 100

        body = {"host": host, "sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IFederationFollower](
            self.__session, Route("POST", "/api/federation/followers"), json=body
        )

        while True:
            res_federation_followers: list[IFederationFollower] = await pagination.next()
            for federation_follower in res_federation_followers:
                yield federation_follower

            if get_all is False or pagination.is_final:
                break

    async def get_following(
        self,
        host: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        get_all: bool = False,
    ):
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")

        if get_all:
            limit = 100

        body = {"host": host, "sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IFederationFollowing](
            self.__session, Route("POST", "/api/federation/following"), json=body
        )

        while True:
            res_federation_followings: list[IFederationFollowing] = await pagination.next()
            for federation_following in res_federation_followings:
                yield federation_following

            if get_all is False or pagination.is_final:
                break

    async def get_instances(
        self,
        host: str | None = None,
        blocked: bool | None = None,
        not_responding: bool | None = None,
        suspended: bool | None = None,
        federating: bool | None = None,
        subscribing: bool | None = None,
        publishing: bool | None = None,
        limit: int = 30,
        offset: int = 0,
        sort: str | None = None,
    ) -> list[FederationInstance]:
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")
        body = {
            "host": host,
            "blocked": blocked,
            "notResponding": not_responding,
            "suspended": suspended,
            "federating": federating,
            "subscribing": subscribing,
            "publishing": publishing,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }

        res: list[IFederationInstance] = await self.__session.request(
            Route("POST", "/api/federation/instances"), auth=True, lower=True, json=body
        )

        return [FederationInstance(i, client=self.__client) for i in res]

    async def show_instance(self, host: str) -> FederationInstance:
        res: IFederationInstance = await self.__session.request(
            Route("POST", "/api/federation/show-instance"),
            auth=True,
            json={"host": host},
            lower=True,
        )

        return FederationInstance(res, client=self.__client)

    async def update_remote_user(self, user_id: str) -> bool:
        return bool(
            self.__session.request(
                Route("POST", "/api/federation/update-remote-user"),
                auth=True,
                json={"userId": user_id},
            )
        )

    async def get_users(
        self,
        host: str,
        since_id: str | None = None,
        until_id: str | None = None,
        limit: int = 10,
        get_all: bool = False,
    ) -> AsyncGenerator[UserDetailedNotMe | MeDetailed, None]:
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")

        if get_all:
            limit = 100

        body = {"host": host, "sinceId": since_id, "untilId": until_id, "limit": limit}

        pagination = Pagination[IUserDetailed](
            self.__session, Route("POST", "/api/federation/users"), json=body
        )

        while True:
            res_users: list[IUserDetailed] = await pagination.next()
            for user in res_users:
                yield packed_user(user, client=self.__client)

            if get_all is False or pagination.is_final:
                break

    async def get_stats(self, limit: int = 10) -> IFederationInstanceStat:
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")
        res: IFederationInstanceStat = await self.__session.request(
            Route("POST", "/api/federation/stats"), auth=True, body={"limit": limit}, lower=True
        )
        return res
