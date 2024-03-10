from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from mipac.models.lite.ad import PartialAd
from mipac.types.ads import IAd
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Ad(PartialAd[IAd]):
    def __init__(self, ad_data: IAd, *, client: ClientManager) -> None:
        super().__init__(ad_data, client=client)

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
    def priority(self) -> Literal["high" "middle" "low"]:
        """広告の優先度

        Returns
        -------
        Literal["high" "middle" "low"]
            広告の優先度
        """
        return self._raw_ad["priority"]

    @property
    def memo(self) -> str | None:
        """広告のメモ

        Returns
        -------
        str | None
            広告のメモ
        """
        return self._raw_ad["memo"]
