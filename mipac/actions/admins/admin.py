from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.abstract.action import AbstractAction

from mipac.errors.base import NotSupportVersion, ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.admin import ModerationLog, ServerInfo
from mipac.models.meta import AdminMeta
from mipac.types.admin import IModerationLog, IServerInfo
from mipac.types.meta import IAdminMeta, IUpdateMetaBody
from mipac.config import config
from mipac.util import cache, convert_dict_keys_to_camel

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class AdminActions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session = session
        self.__client = client

    async def get_meta(self, detail: bool = False) -> AdminMeta:
        res: IAdminMeta = await self.__session.request(
            Route('POST', '/api/admin/meta'), json={'detail': detail}, auth=True, lower=True,
        )
        return AdminMeta(res, client=self.__client)

    async def get_invite(self) -> bool:
        return bool(await self.__session.request(Route('POST', '/api/admin/invite')))

    async def vacuum(self, full: bool = False, analyze: bool = False) -> bool:
        body = {'full': full, 'analyze': analyze}
        return bool(
            await self.__session.request(Route('POST', '/api/admin/vacuum'), auth=True, json=body)
        )

    async def update_user_note(self, user_id: str, text: str) -> bool:
        if config.use_version < 12:
            raise NotSupportVersion('ご利用のインスタンスのバージョンではサポートされていない機能です')
        body = {'userId': user_id, 'text': text}
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/update-user-note'), auth=True, json=body
            )
        )

    async def update_meta(self, meta: IUpdateMetaBody) -> bool:
        body = convert_dict_keys_to_camel(
            meta, replace_list={'tos_text_url': 'ToSTextUrl', 'tos_url': 'ToSUrl'}
        )

        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/update-meta'),
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
                Route('POST', '/api/admin/unsuspend-user'), json={'userId': user_id}, auth=True
            )
        )

    async def unsilence_user(self, user_id: str) -> bool:
        """Unsilence user with specified Id

        Parameters
        ----------
        user_id : str
            Id of user to unsilence

        Returns
        -------
        bool
            success or failed
        """

        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/unsilence-user'), json={'userId': user_id}, auth=True
            )
        )

    async def suspend_user(self, user_id: str) -> bool:
        """Suspends the user for the specified Id

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
                Route('POST', '/api/admin/suspend-user'), json={'userId': user_id}, auth=True
            )
        )

    async def silence_user(self, user_id: str) -> bool:
        """Silences the user of the specified Id

        Parameters
        ----------
        user_id : str
            Id of user to silence

        Returns
        -------
        bool
            success or failed
        """
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/silence-user'), json={'userId': user_id}, auth=True
            )
        )

    async def get_moderation_logs(
        self, limit: int = 10, since_id: str | None = None, until_id: str | None = None
    ) -> ModerationLog:
        if limit > 100:
            raise ParameterError('limit must be less than 100')
        body = {'limit': limit, 'sinceId': since_id, 'untilId': until_id}
        moderation_log_payload: IModerationLog = await self.__session.request(
            Route('POST', '/api/admin/show-moderation-logs'), json=body, auth=True, lower=True
        )
        return ModerationLog(moderation_log_payload, client=self.__client)

    @cache('server_info')
    async def get_server_info(self, **kwargs) -> ServerInfo:
        server_info_payload: IServerInfo = await self.__session.request(
            Route('POST', '/api/admin/server-info'), auth=True, lower=True
        )
        return ServerInfo(server_info_payload)

    async def fetch_server_info(self) -> ServerInfo:
        return await self.get_server_info(cache_override=True)

    async def send_mail(self, to: str, subject: str, text: str) -> bool:
        body = {'to': to, 'subject': subject, 'text': text}
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/send-email'), auth=True, json=body
            )
        )

    async def resolve_abuse_user_report(self, report_id: str, forward: bool = False) -> bool:
        body = {'reportId': report_id, 'forward': forward}
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/resolve-abuse-user-report'), auth=True, json=body
            )
        )

    async def reset_password(self, user_id: str) -> str:
        """指定したIDのユーザーのパスワードをリセットします

        Parameters
        ----------
        user_id : str
            パスワードをリセットする対象のユーザーID

        Returns
        -------
        str
            新しいパスワード
        """
        return await self.__session.request(
            Route('POST', '/api/admin/reset-password'), auth=True, json={'userId': user_id}
        )
