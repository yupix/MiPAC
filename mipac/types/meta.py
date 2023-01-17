from typing import TypedDict
from mipac.types.ads import IAds

from mipac.types.emoji import ICustomEmoji


class ICPU(TypedDict):
    cores: int
    model: str


class IPolicies(TypedDict):
    gtl_available: bool
    ltl_available: bool
    can_public_note: bool
    can_invite: bool
    can_manage_custom_emojis: bool
    can_hide_ads: bool
    drive_capacity_mb: int
    pin_limit: int
    antenna_limit: int
    word_mute_limit: int
    webhook_limit: int
    clip_limit: int
    note_each_clips_limit: int
    user_list_limit: int
    user_each_user_lists_limit: int
    rate_limit_factor: int


class IAnnouncement(TypedDict):
    image: str | None
    text: str
    title: str


class IV12Features(TypedDict):
    email_required_for_signup: bool


class IAyuskeyFeatures(TypedDict):
    miauth: bool


class IV11Features(TypedDict):
    global_time_line: bool
    local_time_line: bool


class IFeatures(IV12Features, IV11Features, IAyuskeyFeatures):
    registration: bool
    elasticsearch: bool
    hcaptcha: bool
    recaptcha: bool
    object_storage: bool
    twitter: bool
    github: bool
    discord: bool
    service_worker: bool


class ILiteV12Meta(TypedDict, total=False):
    ads: list[IAds]
    background_image_url: str
    default_dark_theme: str
    default_light_theme: str
    email_required_for_signup: bool
    logo_image_url: str
    translator_available: bool  # v12 only
    theme_color: str


class ILiteV11Meta(TypedDict, total=False):
    announcements: list[IAnnouncement]
    blocked_hosts: list[str]
    cpu: ICPU
    disable_local_timeline: bool
    disable_global_timeline: bool
    discord_client_id: str
    discord_client_secret: str
    drive_capacity_per_local_user_mb: int
    drive_capacity_per_remote_user_mb: int
    email: str
    enable_emoji_reaction: bool
    github_client_id: str
    github_client_secret: str
    hidden_tags: list[str]
    machine: str
    node: str
    object_storage_access_key: str
    object_storage_base_url: str
    object_storage_bucket: str
    object_storage_endpoint: str
    object_storage_port: int
    object_storage_prefix: str
    object_storage_region: str
    object_storage_s3_force_path_style: bool
    object_storage_secret_key: str
    object_storage_set_public_read: bool
    object_storage_use_proxy: bool
    object_storage_use_ssl: bool
    os: str
    pinned_users: list[str]
    proxy_account: str
    proxy_remote_files: bool
    psql: str
    recaptcha_secret_key: str
    redis: str
    secure: bool
    smtp_host: str
    smtp_pass: str
    smtp_port: int
    smtp_secure: bool
    smtp_user: str
    summaly_proxy: str
    sw_private_key: str
    tos_text_url: str
    turnstile_secret_key: str
    twitter_consumer_key: str
    twitter_consumer_secret: str
    use_object_storage: bool
    use_star_for_reaction_fallback: bool


class IV12AndV11Meta(TypedDict, total=False):
    emojis: list[ICustomEmoji]


class ILiteMeta(ILiteV12Meta, ILiteV11Meta, IV12AndV11Meta):
    banner_url: str | None
    cache_remote_files: bool
    description: str | None
    disable_registration: bool
    enable_discord_integration: bool
    enable_github_integration: bool
    enable_service_worker: bool
    enable_twitter_integration: bool
    feedback_url: str
    maintainer_email: str | None
    maintainer_name: str | None
    max_note_text_length: int
    name: str | None
    recaptcha_site_key: str
    repository_url: str
    sw_publickey: str | None
    tos_url: str  # 厳密にはv11とv12で異なるが、スネークケースに置き換える都合上問題ない
    uri: str
    version: str


class IV12Meta(TypedDict, total=False):
    pinned_clip_id: str
    proxy_account_name: str
    pinned_pages: list[str]
    policies: IPolicies
    require_setup: bool


class IMeta(ILiteMeta, IV12Meta):
    features: IFeatures


class IV12AdminMeta:
    pass


class ISharedAdminMeta:
    pass


class IAdminMeta:
    pass
