"""MiPACで使用する設定を保持するクラスを定義するモジュール"""

from dataclasses import dataclass
from typing import Self


@dataclass
class CacheConfigData:
    """キャッシュの設定を保持するクラス"""

    maxsize: int = 1024
    ttl: int = 360


class CacheConfig:
    """キャッシュの設定を保持するクラス"""

    def __init__(self, options: CacheConfigData) -> None:
        self.maxsize: int = options.maxsize
        self.ttl: int = options.ttl


class Config:
    """MiPACで使用する設定を保持するクラス"""

    def __init__(
        self,
        *,
        host: str = "",
        is_ssl: bool = True,
        cache: CacheConfigData | None = None,
    ) -> None:
        self.is_ssl: bool = is_ssl
        self.host: str = host
        self.cache: CacheConfig = CacheConfig(cache or CacheConfigData())

    def from_dict(
        self,
        *,
        host: str | None = None,
        is_ssl: bool | None = None,
        cache: CacheConfigData | None = None,
    ) -> Self:
        """dictから設定を更新します

        Parameters
        ----------
        host : str | None, optional
            サーバーのhost, by default None
        is_ssl : bool | None, optional
            サーバーがsslかどうか, by default None
        cache : CacheConfigData | None, optional
            キャッシュの設定, by default None

        Returns
        -------
        Self
            更新されたConfigクラス
        """
        self.host = host or self.host
        self.is_ssl = is_ssl if is_ssl is not None else self.is_ssl
        if cache:
            self.cache = CacheConfig(cache)
        return self


config = Config()
