from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.types.instance import IFederationInstance

if TYPE_CHECKING:
    from mipac.client import ClientManager


class FederationInstance:
    def __init__(
        self, instance: IFederationInstance, *, client: ClientManager
    ) -> None:
        self.__instance: IFederationInstance = instance
        self.__client: ClientManager = client

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
