from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement, AnnouncementDetailed
from mipac.types.announcement import IAnnouncement, IAnnouncementDetailed
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class SharedAdminAnnouncementActions(AbstractAction):
    def __init__(
        self,
        *,
        session: HTTPClient,
        client: ClientManager,
    ) -> None:
        self._session: HTTPClient = session
        self._client: ClientManager = client

    async def delete(self, *, announce_id: str) -> bool:
        res: bool = await self._session.request(
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
        announce_id: str,
    ):
        body = {
            "id": announce_id,
            "title": title,
            "text": text,
            "imageUrl": image_url,
        }
        res: bool = await self._session.request(
            Route("POST", "/api/admin/announcements/update"),
            json=body,
            auth=True,
            remove_none=False,
        )
        return res


class ClientAdminAnnouncementActions(SharedAdminAnnouncementActions):
    def __init__(
        self,
        announce_id: str,
        *,
        session: HTTPClient,
        client: ClientManager,
    ) -> None:
        super().__init__(session=session, client=client)
        self.__announce_id: str = announce_id

    @override
    async def delete(self, *, announce_id: str | None = None) -> bool:
        announce_id = announce_id or self.__announce_id
        return await super().delete(announce_id=announce_id)

    @override
    async def update(
        self,
        title: str,
        text: str,
        image_url: str | None = None,
        *,
        announce_id: str | None = None,
    ):
        announce_id = announce_id or self.__announce_id
        return await super().update(
            title=title, text=text, image_url=image_url, announce_id=announce_id
        )


class AdminAnnouncementActions(SharedAdminAnnouncementActions):
    def __init__(
        self,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)

    async def create(self, title: str, text: str, image_url: str | None = None) -> Announcement:
        body = {"title": title, "text": text, "imageUrl": image_url}
        created_announcement: IAnnouncement = await self._session.request(
            Route("POST", "/api/admin/announcements/create"),
            json=body,
            auth=True,
            lower=True,
            remove_none=False,
        )
        return Announcement(created_announcement, client=self._client)

    async def gets(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[AnnouncementDetailed, None]:
        if limit > 100:
            raise ValueError("limitは100以下である必要があります")
        if get_all:
            limit = 100

        body = {
            "limit": limit,
            "sinceId": since_id,
            "untilId": until_id,
        }

        pagination = Pagination[IAnnouncementDetailed](
            self._session, Route("POST", "/api/admin/announcements/list"), json=body
        )

        while True:
            res_annonuncement_systems = await pagination.next()
            for res_announcement_system in res_annonuncement_systems:
                yield AnnouncementDetailed(res_announcement_system, client=self._client)

            if get_all is False or pagination.is_final:
                break
