from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING, Literal

from mipac.types.ads import IAd
from mipac.util import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.admins.ad import AdminAdvertisingModelManager


class Ad:
    def __init__(self, ad_data: IAd, *, client: ClientManager) -> None:
        self.__ad_data: IAd = ad_data
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__ad_data['id']

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__ad_data['created_at'])

    @property
    def starts_at(self) -> datetime:
        return str_to_datetime(self.__ad_data['id'])

    @property
    def expires_at(self) -> datetime:
        return str_to_datetime(self.__ad_data['id'])

    @property
    def url(self) -> str:
        return self.__ad_data['url']

    @property
    def place(self) -> Literal['square' 'horizontal' 'horizontal-big']:
        return self.__ad_data['place']

    @property
    def priority(self) -> Literal['high' 'middle' 'low']:
        return self.__ad_data['priority']

    @property
    def ratio(self) -> int:
        return self.__ad_data['ratio']

    @property
    def image_url(self) -> str:
        return self.__ad_data['image_url']

    @property
    def memo(self) -> str | None:
        return self.__ad_data['memo']

    @property
    def api(self) -> AdminAdvertisingModelManager:
        return self.__client.admin.create_ad_model_manager(ad_id=self.id)
