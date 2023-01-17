from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.lite.instance import LiteInstanceMeta
from mipac.types.instance import IFederationInstance, IInstanceMeta

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('InstanceMeta',)


class FederationInstance:
    def __init__(
        self, instance: IFederationInstance, *, client: ClientActions
    ) -> None:
        self.__instance: IFederationInstance = instance
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__instance['id']

    @property
    def host(self) -> str:
        return self.__instance['host']

    @property
    def users_count(self) -> int:
        return self.__instance['users_count']

    @property
    def notes_count(self) -> int:
        return self.__instance['notes_count']

    @property
    def following_count(self) -> int:
        return self.__instance['following_count']

    @property
    def followers_count(self) -> int:
        return self.__instance['followers_count']

    @property
    def is_not_responding(self) -> bool:
        return self.__instance['is_not_responding']

    @property
    def is_suspended(self) -> bool:
        return self.__instance['is_suspended']

    @property
    def is_blocked(self) -> bool:
        return self.__instance['is_blocked']

    @property
    def software_name(self) -> str:
        return self.__instance['software_name']

    @property
    def software_version(self) -> str:
        return self.__instance['software_version']

    @property
    def open_registrations(self) -> bool:
        return self.__instance['open_registrations']

    @property
    def name(self) -> str:
        return self.__instance['name']

    @property
    def description(self) -> str:
        return self.__instance['description']

    @property
    def maintainer_name(self) -> str:
        return self.__instance['maintainer_name']

    @property
    def maintainer_email(self) -> str:
        return self.__instance['maintainer_email']

    @property
    def icon_url(self) -> str:
        return self.__instance['icon_url']

    @property
    def favicon_url(self) -> str:
        return self.__instance['favicon_url']

    @property
    def theme_color(self) -> str:
        return self.__instance['theme_color']

    @property
    def info_updated_at(self) -> str:
        return self.__instance['info_updated_at']

    @property
    def caught_at(self) -> str | None:
        return self.__instance.get('caught_at')

    @property
    def first_retrieved_at(self) -> str | None:
        return self.__instance.get('first_retrieved_at')

    @property
    def latest_request_sent_at(self) -> str | None:
        return self.__instance.get('latest_request_sent_at')

    @property
    def last_communicated_at(self) -> str | None:
        return self.__instance.get('last_communicated_at')


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
