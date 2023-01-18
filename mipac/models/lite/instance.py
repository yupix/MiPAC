from __future__ import annotations

from mipac.types.instance import IInstanceLite


class LiteInstance:
    def __init__(self, instance: IInstanceLite) -> None:
        self.__instance: IInstanceLite = instance

    @property
    def name(self) -> str:
        return self.__instance['name']

    def software_name(self) -> str:
        return self.__instance['software_name']

    def software_version(self) -> str:
        return self.__instance['software_version']

    def icon_url(self) -> str:
        return self.__instance['icon_url']

    def favicon_url(self) -> str:
        return self.__instance['favicon_url']

    def theme_color(self) -> str:
        return self.__instance['theme_color']
