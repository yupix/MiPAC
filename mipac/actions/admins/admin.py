from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.errors.base import NotSupportVersion
from mipac.http import HTTPClient, Route
from mipac.models.meta import AdminMeta
from mipac.types.meta import IAdminMeta, IUpdateMetaBody
from mipac.config import config
from mipac.util import convert_dict_keys_to_camel

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
