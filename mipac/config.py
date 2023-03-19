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



class ILimits(TypedDict, total=False):
    channel_name: int
    channel_description: int

class IFeatures(TypedDict, total=False):
    chat: bool

class Limits:
    def __init__(self, limits: ILimits | None = None) -> None:
        limits = limits or {}
        self.channel_name: int = limits.get('channel_name', 128)
        self.channel_description: int = limits.get('channel_description', 2048)

    def from_dict(self, limits: ILimits):
        self.channel_name = limits.get('channel_name') or self.channel_description
        self.channel_description = limits.get('channel_description') or self.channel_description
        return self

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
        limits: ILimits | None = None
    ) -> None:
        self.distro: IMisskeyDistribution = distro
        self.is_ssl: bool = is_ssl
        self.host: str = host
        self.is_ayuskey: bool = is_ayuskey
        self.use_version: Literal[13, 12, 11] = use_version
        self.cache: CacheConfig = CacheConfig(cache or CacheConfigData())
        self.use_version_autodetect: bool = use_version_autodetect
        self.features: Features = Features(features) if features else Features()
        self.limits: Limits = Limits(limits) if limits else Limits()

    def from_dict(
        self,
        host: str | None = None,
        is_ssl: bool | None = None,
        is_ayuskey: bool | None = None,
        use_version: Literal[13, 12, 11] | None = None,
        cache: CacheConfigData | None = None,
        use_version_autodetect: bool | None = None,
        features: IFeatures | None = None,
        limits: ILimits | None = None,
    ):
        self.host = host or self.host
        self.is_ssl = is_ssl if is_ssl is not None else self.is_ssl
        self.is_ayuskey = is_ayuskey or self.is_ayuskey
        self.use_version = use_version or self.use_version
        if cache:
            self.cache = CacheConfig(cache)
        self.use_version_autodetect = use_version_autodetect or self.use_version_autodetect
        self.features = self.features.from_dict(features) if features else self.features
        self.limits = self.limits.from_dict(limits) if limits else self.limits


config = Config()
