from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement, AnnouncementSystem
from mipac.types.announcement import IAnnouncement, IAnnouncementSystem

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminAnnouncementClientActions(AbstractAction):
    def __init__(
        self, announce_id: str | None = None, *, session: HTTPClient, client: ClientManager,
    ):
        self.__announce_id = announce_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def delete(self, announce_id: str | None = None) -> bool:
        announce_id = announce_id or self.__announce_id
        res: bool = await self.__session.request(
            Route('POST', '/api/admin/announcements/delete'), json={'id': announce_id}, auth=True,
        )
        return res

    async def update(
        self,
        title: str,
        text: str,
        image_url: str | None = None,
        *,
        announce_id: str | None = None,
    ):
        announce_id = announce_id or self.__announce_id
        body = {
            'id': announce_id,
            'title': title,
            'text': text,
            'imageUrl': image_url,
        }
        res: bool = await self.__session.request(
            Route('POST', '/api/admin/announcements/update'),
            json=body,
            auth=True,
            remove_none=False,
        )
        return res


class AdminAnnouncementActions(AdminAnnouncementClientActions):
    def __init__(
        self, announce_id: str | None = None, *, session: HTTPClient, client: ClientManager,
    ):
        super().__init__(announce_id=announce_id, session=session, client=client)

    async def create(self, title: str, text: str, image_url: str | None = None) -> Announcement:
        body = {'title': title, 'text': text, 'imageUrl': image_url}
        created_announcement: IAnnouncement = await self.__session.request(
            Route('POST', '/api/admin/announcements/create'),
            json=body,
            auth=True,
            lower=True,
            remove_none=False,
        )
        return Announcement(created_announcement, client=self.__client)

    async def gets(
        self, limit: int = 10, since_id: str | None = None, until_id: str | None = None,
    ) -> AsyncGenerator[AnnouncementSystem, None]:
        if limit > 100:
            raise ParameterError('limitは100以下である必要があります')
        if all:
            limit = 100

        async def request(req_body) -> list[AnnouncementSystem]:
            res: list[IAnnouncementSystem] = await self.__session.request(
                Route('POST', '/api/admin/announcements/list'), auth=True, json=req_body,
            )
            return [AnnouncementSystem(announcement, client=self.__client) for announcement in res]

        body = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
        }
        first_req = await request(body)

        for announcement in first_req:
            yield announcement
        if all and len(first_req) == 100:
            body['untilId'] = first_req[-1].id
            while True:
                res = await request(body)
                if len(res) <= 100:
                    for announcement in res:
                        yield announcement
                if len(res) < 100:
                    break
