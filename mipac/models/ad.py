from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.types.ads import IAd, IAdPlaces, IAdPriority
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.admins.ad import ClientAdminAdManager


class Ad:
    def __init__(self, ad_data: IAd, *, client: ClientManager) -> None:
        self._raw_ad: IAd = ad_data
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """広告のID

        Returns
        -------
        str
            広告のID
        """
        return self._raw_ad["id"]

    @property
    def expires_at(self) -> datetime:
        """いつ広告が終了するか

        Returns
        -------
        datetime
            いつ広告が終了するか
        """
        return str_to_datetime(self._raw_ad["expires_at"])

    @property
    def starts_at(self) -> datetime:
        """いつ広告が開始するか

        Returns
        -------
        datetime
            いつ広告が開始するか
        """
        return str_to_datetime(self._raw_ad["starts_at"])

    @property
    def place(self) -> IAdPlaces:
        """広告の掲載場所

        Returns
        -------
        IAdPlaces
            広告の掲載場所
        """
        return self._raw_ad["place"]

    @property
    def priority(self) -> IAdPriority:
        """広告の優先度

        Returns
        -------
        IAdPriority
            広告の優先度
        """
        return self._raw_ad["priority"]

    @property
    def ratio(self) -> int:
        """広告の表示比率

        Returns
        -------
        int
            広告の表示比率
        """
        return self._raw_ad["ratio"]

    @property
    def url(self) -> str:
        """広告のリンク先URL

        Returns
        -------
        str
            広告のリンク先URL
        """
        return self._raw_ad["url"]

    @property
    def image_url(self) -> str:
        """広告の画像URL

        Returns
        -------
        str
            広告の画像URL
        """
        return self._raw_ad["image_url"]

    @property
    def memo(self) -> str:
        """広告のメモ

        Returns
        -------
        str
            広告のメモ
        """
        return self._raw_ad["memo"]

    @property
    def day_of_week(self) -> int:
        return self._raw_ad["day_of_week"]

    @property
    def is_sensitive(self) -> bool:
        """広告がセンシティブかどうか

        Returns
        -------
        bool
            広告がセンシティブかどうか
        """
        return self._raw_ad["is_sensitive"]

    @property
    def api(self) -> ClientAdminAdManager:
        return self.__client.admin._create_client_ad_manager(ad_id=self.id)

    def _get(self, key: str) -> Any | None:
        """You can access the raw response data directly by specifying the key

        Returns
        -------
        Any | None
            raw response data
        """
        return self._raw_ad.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Ad) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
