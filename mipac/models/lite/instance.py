from __future__ import annotations
from typing import Any

from mipac.types.instance import IInstanceLite


class LiteInstance:
    def __init__(self, instance: IInstanceLite) -> None:
        self.__instance: IInstanceLite = instance

    @property
    def name(self) -> str | None:
        return self.__instance["name"]

    @property
    def software_name(self) -> str | None:
        return self.__instance["software_name"]

    @property
    def software_version(self) -> str | None:
        return self.__instance["software_version"]

    @property
    def icon_url(self) -> str | None:
        return self.__instance["icon_url"]

    @property
    def favicon_url(self) -> str | None:
        return self.__instance["favicon_url"]

    @property
    def theme_color(self) -> str | None:
        return self.__instance["theme_color"]

    def _get(self, key: str) -> Any | None:
        return self.__instance.get(key)
