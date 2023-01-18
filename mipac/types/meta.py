from typing import NotRequired, TypedDict
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


class IV12Features(TypedDict, total=False):
    email_required_for_signup: bool
    miauth: bool


class IV11Features(TypedDict, total=False):
    global_time_line: bool
    local_time_line: bool


class IFeatures(IV12Features, IV11Features):
    registration: bool
    elasticsearch: bool
    hcaptcha: bool
    recaptcha: bool
    object_storage: bool
    twitter: bool
    github: bool
    discord: bool
    service_worker: bool


class IV12AdminMeta(TypedDict, total=False):
    hcaptcha_secret_key: str
    sensitive_media_detection: str
    sensitive_media_detection_sensitivity: str
    set_sensitive_flag_automatically: bool
    enable_sensitive_media_detection_for_videos: bool
    proxy_account_id: str
    summary_proxy: str
    enable_ip_logging: bool
    enable_active_email_validation: bool


class ISharedAdminMeta(TypedDict, total=False):
    drive_capacity_per_local_user_mb: int
    drive_capacity_per_remote_user_mb: int
    hidden_tags: list[str]
    blocked_hosts: list[str]
    recaptcha_secret_key: str
    twitter_consumer_key: str
    twitter_consumer_secret: str
    github_client_id: str
    github_client_secret: str
    discord_client_id: str
    discord_client_secret: str
    email: str
    smtp_secure: bool
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    sw_private_key: str
    use_object_storage: bool
    object_storage_base_url: str
    object_storage_bucket: str
    object_storage_prefix: str
    object_storage_endpoint: str
    object_storage_region: str
    object_storage_port: int
    object_storage_access_key: str
    object_storage_secret_key: str
    object_storage_use_ssl: bool
    object_storage_use_proxy: bool
    object_storage_set_public_read: bool
    pinned_users: list[str]


class ILiteV12Meta(TypedDict, total=False):
    background_image_url: str
    default_dark_theme: str
    default_light_theme: str
    logo_image_url: str
    theme_color: str


class IMetaCommonV12(TypedDict, total=False):
    ads: list[IAds]
    translator_available: bool  # v12 only
    email_required_for_signup: bool
    mascot_image_url: str


class ICommonV11(TypedDict, total=False):
    object_storage_s3_force_path_style: bool


class ILiteV11Meta(ICommonV11, total=False):
    announcements: list[IAnnouncement]
    cpu: ICPU
    disable_local_timeline: bool
    disable_global_timeline: bool
    enable_emoji_reaction: bool
    machine: str
    node: str
    os: str
    proxy_account: str
    proxy_remote_files: bool
    psql: str
    redis: str
    secure: bool
    summaly_proxy: str
    tos_text_url: str
    turnstile_secret_key: str


class IMetaCommon(IMetaCommonV12, ICommonV11):
    cache_remote_files: bool
    enable_hcaptch: bool
    hcaptcha_site_key: str | None
    enable_recaptcha: bool
    recaptcha_site_key: str
    sw_publickey: str | None
    banner_url: str | None
    error_image_url: str | None
    icon_url: str | None
    max_note_text_length: int
    enable_email: bool
    enable_twitter_integration: bool
    enable_github_integration: bool
    enable_discord_integration: bool
    enable_service_worker: bool
    proxy_account_name: str | None
    use_star_for_reaction_fallback: bool
    emojis: NotRequired[list[ICustomEmoji]]


class ILiteMeta(IMetaCommon, ILiteV12Meta, ILiteV11Meta, ISharedAdminMeta):
    description: str | None
    disable_registration: bool
    feedback_url: str
    maintainer_email: str | None
    maintainer_name: str | None
    name: str | None
    repository_url: str
    tos_url: str  # 厳密にはv11とv12で異なるが、スネークケースに置き換える都合上問題ない
    uri: str
    version: str


class IV12Meta(TypedDict, total=False):
    pinned_clip_id: str
    pinned_pages: list[str]
    policies: IPolicies
    require_setup: bool


class IMeta(ILiteMeta, IV12Meta):
    features: IFeatures


class IAdminMeta(ISharedAdminMeta, IV12AdminMeta, IMetaCommon):
    pass
