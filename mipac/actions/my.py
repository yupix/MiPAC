from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.follow import FollowRequest
from mipac.types.achievement import IT_ACHIEVEMENT_NAME
from mipac.types.follow import IFollowRequest

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class MyActions(AbstractAction):
    def __init__(self, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def fetch_follow_requests(self) -> list[FollowRequest]:
        res: list[IFollowRequest] = await self.__session.request(
            Route("POST", "/api/following/requests/list"),
            auth=True,
            lower=True,
        )
        return [FollowRequest(i, client=self.__client) for i in res]

    async def get_claim_achievement(self, name: IT_ACHIEVEMENT_NAME) -> bool:
        """指定した名前の実績を解除します

        Parameters
        ----------
        name : 実績名
            解除したい実績の名前

        Returns
        -------
        bool
            成功したか否か

        Raises
        ------
        NotSupportVersion
            実績機能が存在しないサーバーを使用している
        """
        res: bool = await self.__session.request(
            Route("POST", "/api/i/claim-achievement"), auth=True, json={"name": name}, lower=True
        )
        return res
