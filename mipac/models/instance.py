from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.lite.instance import LiteInstanceMeta
from mipac.types.instance import IInstanceMeta

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('InstanceMeta',)


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
