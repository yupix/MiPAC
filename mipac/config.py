from dataclasses import dataclass
from typing import Self, TypedDict


@dataclass
class CacheConfigData:
    maxsize: int = 1024
    ttl: int = 360


class CacheConfig:
    def __init__(self, options: CacheConfigData) -> None:
        self.maxsize: int = options.maxsize
        self.ttl: int = options.ttl


class ILimits(TypedDict, total=False):
    channel_name: int
    channel_description: int


class IFeatures(TypedDict, total=False):
    chat: bool


class Limits:
    def __init__(self, limits: ILimits | None = None) -> None:
        limits = limits or {}
        self.channel_name: int = limits.get("channel_name", 128)
        self.channel_description: int = limits.get("channel_description", 2048)

    def from_dict(self, limits: ILimits):
        self.channel_name = limits.get("channel_name") or self.channel_description
        self.channel_description = limits.get("channel_description") or self.channel_description
        return self


class Features:
    def __init__(self, features: IFeatures | None = None) -> None:
        features = features or {}
        self.chat = features.get("chat", False)

    def from_dict(self, features: IFeatures):
        self.chat = features.get("chat") or self.chat
        return self


class Config:
    def __init__(
        self,
        *,
        host: str = "",
        is_ssl: bool = True,
        cache: CacheConfigData | None = None,
        features: IFeatures | None = None,
        limits: ILimits | None = None,
    ) -> None:
        self.account_id: str = ""
        self.is_ssl: bool = is_ssl
        self.host: str = host
        self.cache: CacheConfig = CacheConfig(cache or CacheConfigData())
        self.features: Features = Features(features) if features else Features()
        self.limits: Limits = Limits(limits) if limits else Limits()

    def from_dict(
        self,
        *,
        host: str | None = None,
        is_ssl: bool | None = None,
        cache: CacheConfigData | None = None,
        features: IFeatures | None = None,
        limits: ILimits | None = None,
        account_id: str | None = None,
    ) -> Self:
        self.host = host or self.host
        self.is_ssl = is_ssl if is_ssl is not None else self.is_ssl
        if cache:
            self.cache = CacheConfig(cache)
        self.features = self.features.from_dict(features) if features else self.features
        self.limits = self.limits.from_dict(limits) if limits else self.limits
        self.account_id = account_id or self.account_id
        return self


config = Config()
