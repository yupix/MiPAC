from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.core.models.instance import RawInstance
from mipac.models.lite.instance import LiteInstanceMeta
from mipac.types.instance import IInstanceMeta

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('Instance',)


class InstanceMeta(LiteInstanceMeta):
    def __init__(
        self, instance: IInstanceMeta, *, client: ClientActions
    ) -> None:
        super().__init__(instance, client=client)
        self.__features = instance['features']

    @property
    def registration(self) -> bool:
        return self.__features['registration']

    @property
    def local_time_line(self) -> bool:
        return self.__features['local_time_line']

    @property
    def global_time_line(self) -> bool:
        return self.__features['global_time_line']

    @property
    def email_required_for_signup(self) -> bool:
        return self.__features['email_required_for_signup']

    @property
    def elasticsearch(self) -> bool:
        return self.__features['elasticsearch']

    @property
    def hcaptcha(self) -> bool:
        return self.__features['hcaptcha']

    @property
    def recaptcha(self) -> bool:
        return self.__features['recaptcha']

    @property
    def object_storage(self) -> bool:
        return self.__features['object_storage']

    @property
    def twitter(self) -> bool:
        return self.__features['twitter']

    @property
    def github(self) -> bool:
        return self.__features['github']

    @property
    def discord(self) -> bool:
        return self.__features['discord']

    @property
    def service_worker(self) -> bool:
        return self.__features['service_worker']

    @property
    def miauth(self) -> bool:
        return self.__features['miauth']


class Instance:
    def __init__(self, raw_data: RawInstance, *, client: ClientActions):
        """
        インスタンス情報

        Parameters
        ----------
        raw_data : RawInstance
            インスタンス情報の入った dict
        """
        self.__raw_data: RawInstance = raw_data
        self.__client: ClientActions = client

    @property
    def host(self):
        return self.__raw_data.host

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def software_name(self):
        return self.__raw_data.software_name

    @property
    def software_version(self):
        return self.__raw_data.software_version

    @property
    def icon_url(self):
        return self.__raw_data.icon_url

    @property
    def favicon_url(self):
        return self.__raw_data.favicon_url

    @property
    def theme_color(self):
        return self.__raw_data.theme_color
