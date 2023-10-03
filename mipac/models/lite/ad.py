from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from mipac.abstract.model import AbstractModel
from mipac.types.ads import IAdPlaces, IPartialAd

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


T = TypeVar("T", bound=IPartialAd)


class PartialAd(AbstractModel, Generic[T]):
    def __init__(self, raw_ad: T, *, client: ClientManager) -> None:
        self._raw_ad: T = raw_ad

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
