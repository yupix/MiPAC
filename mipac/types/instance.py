from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypedDict

from mipac.types.ads import IAds
from mipac.types.emoji import ICustomEmoji

if TYPE_CHECKING:
    from mipac.types.emoji import EmojiPayload

__all__ = (
    'FeaturesPayload',
    'MetaPayload',
    'InstancePayload',
    'OptionalInstance',
    'OptionalMeta',
    'IInstanceLite',
    'IInstanceMeta',
)


class IInstanceLite(TypedDict):
    name: str
    software_name: str
    software_version: str
    icon_url: str
    favicon_url: str
    theme_color: str


class FeaturesPayload(TypedDict):
    registration: bool
    local_time_line: bool
    global_time_line: bool
    email_required_for_signup: bool
    elasticsearch: bool
    hcaptcha: bool
    recaptcha: bool
    object_storage: bool
    twitter: bool
    github: bool
    discord: bool
    service_worker: bool
    miauth: bool


class OptionalMeta(TypedDict, total=False):
    pinned_page: list[str]
    cache_remote_files: bool
    proxy_remote_files: bool
    require_setup: bool
    features: FeaturesPayload


class MetaPayload(OptionalMeta):
    maintainer_name: str
    maintainer_email: str
    version: str
    name: str
    uri: str
    description: str
    langs: list[str]
    tos_url: Optional[str]
    repository_url: str
    feedback_url: str
    secure: bool
    disable_registration: bool
    disable_local_timeline: bool
    disable_global_timeline: bool
    drive_capacity_per_local_user_mb: int
    drive_capacity_per_remote_user_mb: int
    email_required_for_signup: bool
    enable_hcaptcha: bool
    enable_recaptcha: bool
    recaptcha_site_key: str
    sw_publickey: str
    mascot_image_url: str
    error_image_url: str
    max_note_text_length: int
    emojis: list[EmojiPayload]
    ads: list
    enable_email: bool
    enable_twitter_integration: bool
    enable_github_integration: bool
    enable_discord_integration: bool
    enable_service_worker: bool
    translator_available: bool


class IInstanceMetaLiteRequired(TypedDict):
    version: str
    uri: str
    disable_registration: bool
    disable_local_timeline: bool
    disable_global_timeline: bool
    drive_capacity_per_local_user_mb: int
    drive_capacity_per_remote_user_mb: int
    enable_hcaptcha: bool
    max_note_text_length: int
    enable_email: bool
    enable_twitter_integration: bool
    enable_github_integration: bool
    enable_discord_integration: bool
    enable_service_worker: bool
    emojis: list[ICustomEmoji]
    mascot_image_url: str
    banner_url: str
    icon_url: str


class IInstanceMetaLite(IInstanceMetaLiteRequired, total=False):
    maintainer_name: str
    maintainer_email: str
    name: str
    description: str
    langs: list[str]
    tos_url: str
    tos_text_url: str
    announcements: dict[str, Any]
    hcaptcha_site_key: str
    enable_recaptcha: bool
    recaptcha_siteKey: str
    sw_publickey: str
    ads: list[IAds]  # v12 only


class IInstanceMeta(IInstanceMetaLite):
    features: FeaturesPayload


class OptionalInstance(TypedDict, total=False):
    host: str
    software_name: str
    software_version: str
    icon_url: str
    favicon_url: str
    theme_color: str


class InstancePayload(OptionalInstance, MetaPayload):
    meta: MetaPayload
