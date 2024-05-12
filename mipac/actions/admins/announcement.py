from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, override

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient, Route
from mipac.models.announcement import Announcement, AnnouncementDetailed
from mipac.types.announcement import (
    AnnouncementDisplay,
    AnnoucementIcon,
    IAnnouncement,
    IAnnouncementDetailed,
)
from mipac.utils.format import remove_dict_missing
from mipac.utils.pagination import Pagination
from mipac.utils.util import MISSING

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
        """指定したお知らせを削除します

        Parameters
        ----------
        announce_id : str
            削除したいお知らせのID

        Returns
        -------
        bool
            削除に成功した場合はTrue, それ以外はFalse
        """
        res: bool = await self._session.request(
            Route("POST", "/api/admin/announcements/delete"),
            json={"id": announce_id},
            auth=True,
        )
        return res

    async def update(
        self,
        title: str = MISSING,
        text: str = MISSING,
        image_url: str | None = MISSING,
        icon: AnnoucementIcon = MISSING,
        display: AnnouncementDisplay = MISSING,
        for_existing_users: bool = MISSING,
        silence: bool = MISSING,
        need_confirmation_to_read: bool = MISSING,
        is_active: bool = MISSING,
        *,
        announce_id: str,
    ) -> bool:
        """指定したお知らせを更新します

        Parameters
        ----------
        title : str
            お知らせのタイトル
        text : str
            お知らせの本文
        image_url : str, optional
            お知らせの画像URL, by default None
        icon : AnnoucementIcon, optional
            お知らせのアイコン, by default MISSING
        display : AnnouncementDisplay, optional
            お知らせの表示方法, by default MISSING
        for_existing_users : bool, optional
            既存ユーザーに表示するか, by default MISSING
        silence : bool, optional
            お知らせを静かにするか, by default MISSING
        need_confirmation_to_read : bool, optional
            読んだか確認が必要か, by default MISSING
        is_active : bool, optional
            お知らせが有効かどうか, by default MISSING
        announce_id : str
            更新したいお知らせのID

        Returns
        -------
        bool
            更新に成功した場合はTrue, それ以外はFalse
        """
        if image_url and len(image_url) < 1:  # image_urlはNoneの場合があるので別枠でチェック
            raise ValueError("image_url must not be empty")

        body = remove_dict_missing(
            {
                "id": announce_id,
                "title": title,
                "text": text,
                "imageUrl": image_url,
                "icon": icon,
                "display": display,
                "forExistingUsers": for_existing_users,
                "silence": silence,
                "needConfirmationToRead": need_confirmation_to_read,
                "isActive": is_active,
            }
        )

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
        title: str = MISSING,
        text: str = MISSING,
        image_url: str | None = MISSING,
        icon: AnnoucementIcon = MISSING,
        display: AnnouncementDisplay = MISSING,
        for_existing_users: bool = MISSING,
        silence: bool = MISSING,
        need_confirmation_to_read: bool = MISSING,
        is_active: bool = MISSING,
        *,
        announce_id: str | None = None,
    ) -> bool:
        announce_id = announce_id or self.__announce_id

        return await super().update(
            title=title,
            text=text,
            image_url=image_url,
            icon=icon,
            display=display,
            for_existing_users=for_existing_users,
            silence=silence,
            need_confirmation_to_read=need_confirmation_to_read,
            is_active=is_active,
            announce_id=announce_id,
        )


class AdminAnnouncementActions(SharedAdminAnnouncementActions):
    def __init__(
        self,
        *,
        session: HTTPClient,
        client: ClientManager,
    ):
        super().__init__(session=session, client=client)

    async def create(
        self,
        title: str,
        text: str,
        image_url: str | None = None,
        icon: AnnoucementIcon = MISSING,
        display: AnnouncementDisplay = MISSING,
        for_existing_users: bool = MISSING,
        silence: bool = MISSING,
        need_confirmation_to_read: bool = MISSING,
        user_id: str = MISSING,
    ) -> Announcement:
        body = remove_dict_missing(
            {
                "title": title,
                "text": text,
                "imageUrl": image_url,
                "icon": icon,
                "display": display,
                "forExistingUsers": for_existing_users,
                "silence": silence,
                "needConfirmationToRead": need_confirmation_to_read,
                "userId": user_id,
            }
        )
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
    ) -> AsyncGenerator[AnnouncementDetailed, None]:  # TODO: 戻り値を改めて確認するべき
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
