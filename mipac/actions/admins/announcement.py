from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement, AnnouncementSystem
from mipac.types.announcement import IAnnouncement, IAnnouncementSystem
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminAnnouncementClientActions(AbstractAction):
    def __init__(
        self,
        announce_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        self.__announce_id = announce_id
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def delete(self, announce_id: str | None = None) -> bool:
        announce_id = announce_id or self.__announce_id
        res: bool = await self.__session.request(
            Route("POST", "/api/admin/announcements/delete"),
            json={"id": announce_id},
            auth=True,
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
            "id": announce_id,
            "title": title,
            "text": text,
            "imageUrl": image_url,
        }
        res: bool = await self.__session.request(
            Route("POST", "/api/admin/announcements/update"),
            json=body,
            auth=True,
            remove_none=False,
        )
        return res


class AdminAnnouncementActions(AdminAnnouncementClientActions):
    def __init__(
        self,
        announce_id: str | None = None,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(announce_id=announce_id, session=session, client=client)

    async def create(self, title: str, text: str, image_url: str | None = None) -> Announcement:
        body = {"title": title, "text": text, "imageUrl": image_url}
        created_announcement: IAnnouncement = await self.__session.request(
            Route("POST", "/api/admin/announcements/create"),
            json=body,
            auth=True,
            lower=True,
            remove_none=False,
        )
        return Announcement(created_announcement, client=self.__client)

    async def gets(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[AnnouncementSystem, None]:
        if limit > 100:
            raise ParameterError("limitは100以下である必要があります")
        if get_all:
            limit = 100

        body = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        pagination = Pagination[IAnnouncementSystem](
            self.__session, Route("POST", "/api/admin/announcements/list"), json=body
        )

        while True:
            res_annonuncement_systems = await pagination.next()
            for res_announcement_system in res_annonuncement_systems:
                yield AnnouncementSystem(res_announcement_system, client=self.__client)

            if get_all is False or pagination.is_final:
                break
