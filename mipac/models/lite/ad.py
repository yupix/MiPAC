from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from mipac.types.ads import IAdPlaces, IPartialAd

if TYPE_CHECKING:
    from mipac.manager.admins.ad import ClientAdminAdManager
    from mipac.manager.client import ClientManager


T = TypeVar("T", bound=IPartialAd)


class PartialAd[T: IPartialAd]:
    def __init__(self, raw_ad: T, *, client: ClientManager) -> None:
        self._raw_ad: T = raw_ad
        self._client = client

    @property
    def id(self) -> str:
        return self._raw_ad["id"]

    @property
    def url(self) -> str:
        return self._raw_ad["url"]

    @property
    def place(self) -> IAdPlaces:
        return self._raw_ad["place"]

    @property
    def ratio(self) -> int:
        return self._raw_ad["ratio"]

    @property
    def image_url(self) -> str:
        return self._raw_ad["image_url"]

    @property
    def day_of_week(self) -> int:
        return self._raw_ad["day_of_week"]

    @property
    def api(self) -> ClientAdminAdManager:
        return self._client.admin._create_client_ad_manager(ad_id=self.id)

    def _get(self, key: str) -> Any | None:
        """You can access the raw response data directly by specifying the key


        Returns
        -------
        Any | None
            raw response data
        """
        return self._raw_ad.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialAd) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
