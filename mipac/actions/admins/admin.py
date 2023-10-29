from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from mipac.abstract.action import AbstractAction
from mipac.config import config
from mipac.errors.base import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.admin import IndexStat, ModerationLog, ServerInfo, UserIP
from mipac.models.meta import AdminMeta
from mipac.models.user import MeDetailed, UserDetailed
from mipac.types.admin import IIndexStat, IModerationLog, IServerInfo, ITableStats, IUserIP
from mipac.types.meta import IAdminMeta, IUpdateMetaBody
from mipac.types.user import IMeDetailed, IUserDetailed, is_me_detailed
from mipac.utils.cache import cache
from mipac.utils.format import convert_dict_keys_to_camel
from mipac.utils.pagination import Pagination

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_meta(self, detail: bool = False) -> AdminMeta:
        """
        Get admin meta
        Endpoint: `/api/admin/meta`

        Parameters
        ----------
        detail : bool, optional
            flag of detail, by default False
        """
        res: IAdminMeta = await self.__session.request(
            Route("POST", "/api/admin/meta"),
            json={"detail": detail},  # 現状detailがあってもなんも変わらない
            auth=True,
            lower=True,
        )
        return AdminMeta(res, client=self.__client)

    async def vacuum(self, full: bool = False, analyze: bool = False) -> bool:
        body = {"full": full, "analyze": analyze}
        return bool(
            await self.__session.request(Route("POST", "/api/admin/vacuum"), auth=True, json=body)
        )

    async def update_user_note(self, user_id: str, text: str) -> bool:
        """
        Update user note
        Endpoint: `/api/admin/update-user-note`

        Parameters
        ----------
        user_id : str
            target user's id
        text : str
            new note
        """
        body = {"userId": user_id, "text": text}
        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/update-user-note"), auth=True, json=body
            )
        )

    async def update_meta(self, meta: IUpdateMetaBody) -> bool:
        body = convert_dict_keys_to_camel(
            meta, replace_list={"tos_text_url": "ToSTextUrl", "tos_url": "ToSUrl"}
        )

        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/update-meta"),
                json=body,
                auth=True,
                lower=True,
                remove_none=False,
            )
        )

    async def unsuspend_user(self, user_id: str) -> bool:
        """Unsuspend user with specified Id

        Parameters
        ----------
        user_id : str
            Id of user to unsuspend

        Returns
        -------
        bool
            success or failed
        """

        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/unsuspend-user"), json={"userId": user_id}, auth=True
            )
        )

    async def suspend_user(self, user_id: str) -> bool:
        """
        Suspends the user for the specified Id
        Endpoint: `/api/admin/suspend-user`

        Parameters
        ----------
        user_id : str
            Id of user to suspend

        Returns
        -------
        bool
            success or failed
        """
        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/suspend-user"), json={"userId": user_id}, auth=True
            )
        )

    async def get_moderation_logs(
        self,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        get_all: bool = False,
    ) -> AsyncGenerator[ModerationLog, None]:
        if limit > 100:
            raise ParameterError("limit must be less than 100")

        if get_all:
            limit = 100

        body = {"limit": limit, "sinceId": since_id, "untilId": until_id}
        pagination = Pagination[IModerationLog](
            self.__session, Route("POST", "/api/admin/show-moderation-logs"), json=body
        )

        while True:
            res_moderation_logs = await pagination.next()
            for res_moderation_log in res_moderation_logs:
                yield ModerationLog(res_moderation_log, client=self.__client)

    @cache("server_info")
    async def get_server_info(self, **kwargs) -> ServerInfo:
        server_info_payload: IServerInfo = await self.__session.request(
            Route("POST", "/api/admin/server-info"), auth=True, lower=True
        )
        return ServerInfo(server_info_payload)

    async def fetch_server_info(self) -> ServerInfo:
        return await self.get_server_info(cache_override=True)

    async def send_email(self, to: str, subject: str, text: str) -> bool:
        """
        Send email to specified address
        Endpoint: `/api/admin/send-email`

        Parameters
        ----------
        to : str
            email address to send
        subject : str
            email subject
        text : str
            email body
        """
        body = {"to": to, "subject": subject, "text": text}
        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/send-email"), auth=True, json=body
            )
        )

    async def resolve_abuse_user_report(self, report_id: str, forward: bool = False) -> bool:
        """
        Resolve abuse user report
        Endpoint: `/api/admin/resolve-abuse-user-report`

        Parameters
        ----------
        report_id : str
            report id
        forward : bool, optional
            Whether to forward the report to a remote server
        """
        body = {"reportId": report_id, "forward": forward}
        return bool(
            await self.__session.request(
                Route("POST", "/api/admin/resolve-abuse-user-report"), auth=True, json=body
            )
        )

    async def reset_password(self, user_id: str) -> str:
        """
        target user's password reset
        Endpoint: `/api/admin/reset-password`

        Parameters
        ----------
        user_id : str
            target user's id

        Returns
        -------
        str
            new password
        """
        return await self.__session.request(
            Route("POST", "/api/admin/reset-password"), auth=True, json={"userId": user_id}
        )

    async def get_table_stats(self) -> dict[str, ITableStats]:
        return await self.__session.request(Route("POST", "/api/admin/get-table-stats"), auth=True)

    async def get_index_stats(self) -> list[IndexStat]:
        res: list[IIndexStat] = await self.__session.request(
            Route("POST", "/api/admin/get-index-stats"), auth=True
        )
        return [IndexStat(i) for i in res]

    async def get_user_ips(self, user_id: str) -> list[UserIP]:
        res: list[IUserIP] = await self.__session.request(
            Route("POST", "/api/admin/get-user-ips"),
            auth=True,
            json={"userId": user_id},
            lower=True,
        )
        return [UserIP(i) for i in res]

    async def show_user(self, user_id: str) -> UserDetailed:
        res: IUserDetailed = await self.__session.request(
            Route("POST", "/api/admin/show-user"), auth=True, json={"userId": user_id}
        )
        return UserDetailed(res, client=self.__client)

    async def show_users(
        self,
        limit: int = 10,
        offset: int = 0,
        sort: str | None = None,
        state: str = "all",
        origin: str = "combined",
        username: str | None = None,
        hostname: str | None = None,
    ) -> list[MeDetailed | UserDetailed]:
        body = {
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "state": state,
            "origin": origin,
            "username": username,
            "hostname": hostname,
        }
        res: list[IMeDetailed | IUserDetailed] = await self.__session.request(
            Route("POST", "/api/admin/show-users"), auth=True, json=body
        )

        return [
            MeDetailed(i, client=self.__client)
            if is_me_detailed(i, config.account_id)
            else UserDetailed(i, client=self.__client)
            for i in res
        ]
