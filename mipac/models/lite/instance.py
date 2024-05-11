from __future__ import annotations
from typing import Any

from mipac.types.instance import IInstanceLite


class LiteInstance:
    def __init__(self, instance: IInstanceLite) -> None:
        self.__instance: IInstanceLite = instance

    @property
    def name(self) -> str | None:
        """サーバー名

        Returns
        -------
        str | None
            サーバー名
        """
        return self.__instance["name"]

    @property
    def software_name(self) -> str | None:
        """使用しているソフトウェアの名前

        Returns
        -------
        str | None
            使用しているソフトウェアの名前
        """
        return self.__instance["software_name"]

    @property
    def software_version(self) -> str | None:
        """使用しているソフトウェアのバージョン

        Returns
        -------
        str | None
            使用しているソフトウェアのバージョン
        """
        return self.__instance["software_version"]

    @property
    def icon_url(self) -> str | None:
        """アイコンのURL

        Returns
        -------
        str | None
            アイコンのURL
        """
        return self.__instance["icon_url"]

    @property
    def favicon_url(self) -> str | None:
        """ファビコンのURL

        Returns
        -------
        str | None
            ファビコンのURL
        """
        return self.__instance["favicon_url"]

    @property
    def theme_color(self) -> str | None:
        """テーマカラー

        Returns
        -------
        str | None
            テーマカラー

        """
        return self.__instance["theme_color"]

    def _get(self, key: str) -> Any | None:
        return self.__instance.get(key)
