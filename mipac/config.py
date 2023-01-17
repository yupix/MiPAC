from dataclasses import dataclass
from typing import Literal


@dataclass
class CacheConfigData:
    maxsize: int = 1024
    ttl: int = 360


class CacheConfig:
    def __init__(self, options: CacheConfigData) -> None:
        self.maxsize: int = options.maxsize
        self.ttl: int = options.ttl


class Config:
    def __init__(
        self,
        host: str = '',
        is_ssl: bool = True,
        is_ayuskey: bool = False,
        use_version: Literal[13, 12, 11] = 12,
        cache: CacheConfigData | None = None,
    ) -> None:
        self.is_ssl: bool = is_ssl
        self.host: str = host
        self.is_ayuskey: bool = is_ayuskey
        self.use_version: Literal[13, 12, 11] = use_version
        self.cache: CacheConfig = CacheConfig(cache or CacheConfigData())

    def from_dict(
        self,
        host: str | None = None,
        is_ssl: bool | None = None,
        is_ayuskey: bool | None = None,
        use_version: Literal[13, 12, 11] | None = None,
        cache: CacheConfigData | None = None,
    ):
        self.host = host or self.host
        self.is_ssl = is_ssl if is_ssl is not None else self.is_ssl
        self.is_ayuskey = is_ayuskey or self.is_ayuskey
        self.use_version = use_version or self.use_version
        if cache:
            self.cache = CacheConfig(cache)


config = Config()
