from dataclasses import dataclass
from typing import Literal, TypedDict


@dataclass
class CacheConfigData:
    maxsize: int = 1024
    ttl: int = 360


class CacheConfig:
    def __init__(self, options: CacheConfigData) -> None:
        self.maxsize: int = options.maxsize
        self.ttl: int = options.ttl


IMisskeyDistribution = Literal['ayuskey', 'm544', 'areionskey', 'official']


class IFeatures(TypedDict, total=False):
    chat: bool


class Features:
    def __init__(self, features: IFeatures | None = None) -> None:
        features = features or {}
        self.chat = features.get('chat', False)

    def from_dict(self, features: IFeatures):
        self.chat = features.get('chat') or self.chat
        return self


class Config:
    def __init__(
        self,
        host: str = '',
        is_ssl: bool = True,
        distro: IMisskeyDistribution = 'official',
        is_ayuskey: bool = False,
        use_version: Literal[13, 12, 11] = 12,
        cache: CacheConfigData | None = None,
        use_version_autodetect: bool = True,
        features: IFeatures | None = None,
    ) -> None:
        self.distro: IMisskeyDistribution = distro
        self.is_ssl: bool = is_ssl
        self.host: str = host
        self.is_ayuskey: bool = is_ayuskey
        self.use_version: Literal[13, 12, 11] = use_version
        self.cache: CacheConfig = CacheConfig(cache or CacheConfigData())
        self.use_version_autodetect: bool = use_version_autodetect
        self.features: Features = Features(features) if features else Features()

    def from_dict(
        self,
        host: str | None = None,
        is_ssl: bool | None = None,
        is_ayuskey: bool | None = None,
        use_version: Literal[13, 12, 11] | None = None,
        cache: CacheConfigData | None = None,
        use_version_autodetect: bool | None = None,
        features: IFeatures | None = None,
    ):
        self.host = host or self.host
        self.is_ssl = is_ssl if is_ssl is not None else self.is_ssl
        self.is_ayuskey = is_ayuskey or self.is_ayuskey
        self.use_version = use_version or self.use_version
        if cache:
            self.cache = CacheConfig(cache)
        self.use_version_autodetect = use_version_autodetect or self.use_version_autodetect
        self.features = self.features.from_dict(features) if features else self.features


config = Config()
