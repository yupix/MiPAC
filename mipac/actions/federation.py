from __future__ import annotations

from typing import TYPE_CHECKING, Any
from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.instance import FederationInstance
from mipac.types.follow import IFederationFollower, IFederationFollowing
from mipac.errors.base import ParameterError
from mipac.types.instance import IFederationInstance, IFederationInstanceStat
from mipac.types.user import IUserDetailed

from mipac.models.user import UserDetailed

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class FederationActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_ap(self, uri: str) -> dict[Any, Any]:
        return dict(await self.__session.request(
            Route('POST', '/api/ap/get'), auth=True, json={'uri': uri}, lower=True
        ))

    async def show_ap(
        self, host: str, since_id: str | None = None, until_id: str | None = None, limit: int = 10
    ) -> FederationInstance:
        body = {'host': host, 'sinceId': since_id, 'untilId': until_id, 'limit': limit}

        res: FederationInstance = await self.__session.request(
            Route('POST', '/api/ap/show'), auth=True, json=body
        )
        return res

    async def get_followers(
        self, host: str, since_id: str | None = None, until_id: str | None = None, limit: int = 10
    ):
        body = {'host': host, 'sinceId': since_id, 'untilId': until_id, 'limit': limit}
        res: list[IFederationFollower] = await self.__session.request(
            Route('POST', '/api/federation/followers'), auth=True, json=body, lower=True
        )
        return res

    async def get_following(
        self, host: str, since_id: str | None = None, until_id: str | None = None, limit: int = 10
    ):
        body = {'host': host, 'sinceId': since_id, 'untilId': until_id, 'limit': limit}
        res: list[IFederationFollowing] = await self.__session.request(
            Route('POST', '/api/federation/following'), auth=True, json=body, lower=True
        )
        return res

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
            raise ParameterError('limitは100以下である必要があります')
        body = {
            'host': host,
            'blocked': blocked,
            'notResponding': not_responding,
            'suspended': suspended,
            'federating': federating,
            'subscribing': subscribing,
            'publishing': publishing,
            'limit': limit,
            'offset': offset,
            'sort': sort,
        }

        res: list[IFederationInstance] = await self.__session.request(
            Route('POST', '/api/federation/instances'), auth=True, lower=True, json=body
        )

        return [FederationInstance(i, client=self.__client) for i in res]

    async def show_instance(self, host: str) -> FederationInstance:
        res: IFederationInstance = await self.__session.request(
            Route('POST', '/api/federation/show-instance'),
            auth=True,
            json={'host': host},
            lower=True,
        )

        return FederationInstance(res, client=self.__client)

    async def update_remote_user(self, user_id: str) -> bool:
        return bool(
            self.__session.request(
                Route('POST', '/api/federation/update-remote-user'),
                auth=True,
                json={'userId': user_id},
            )
        )

    async def get_users(
        self, host: str, since_id: str | None = None, until_id: str | None = None, limit: int = 10
    ) -> UserDetailed:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        body = {'host': host, 'sinceId': since_id, 'untilId': until_id, 'limit': limit}

        res: IUserDetailed = await self.__session.request(
            Route('POST', '/api/federation/users'), auth=True, json=body
        )
        return UserDetailed(res, client=self.__client)

    async def get_stats(self, limit: int = 10) -> IFederationInstanceStat:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        res: IFederationInstanceStat = await self.__session.request(
            Route('POST', '/api/federation/stats'), auth=True, body={'limit': limit}, lower=True
        )
        return res
