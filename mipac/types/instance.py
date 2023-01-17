from __future__ import annotations

from typing import Any, TypedDict

from mipac.types.ads import IAds
from mipac.types.emoji import ICustomEmoji


class IFederationInstanceRequired(TypedDict):
    id: str
    host: str
    users_count: int
    notes_count: int
    following_count: int
    followers_count: int
    is_not_responding: bool
    is_suspended: bool
    is_blocked: bool
    software_name: str
    software_version: str
    open_registrations: bool
    name: str
    description: str
    maintainer_name: str
    maintainer_email: str
    icon_url: str
    favicon_url: str
    theme_color: str
    info_updated_at: str


class IFederationInstance(IFederationInstanceRequired, total=False):
    caught_at: str
    first_retrieved_at: str
    latest_request_sent_at: str
    last_communicated_at: str


class IInstanceLite(TypedDict):
    name: str
    software_name: str
    software_version: str
    icon_url: str
    favicon_url: str
    theme_color: str


class IInstanceFeatures(TypedDict):
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
    mascot_image_url: str
    banner_url: str
    icon_url: str
    description: str
    repository_url: str
    turnstile_site_key: str | None


class IInstanceMetaLite(IInstanceMetaLiteRequired, total=False):
    maintainer_name: str
    maintainer_email: str
    name: str
    langs: list[str]
    tos_url: str
    tos_text_url: str
    announcements: dict[str, Any]
    hcaptcha_site_key: str
    enable_recaptcha: bool
    recaptcha_siteKey: str
    sw_publickey: str
    theme_color: str
    disable_global_timeline: bool  # ayuskey or v11
    disable_local_timeline: bool  # ayuskey or v11
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
    secure: bool
    smtp_host: str
    smtp_pass: str
    smtp_port: str
    smtp_secure: bool
    smtp_user: str
    summaly_proxy: str
    sw_private_key: str
    turnstile_secret_key: str
    twitter_consumer_key: str
    twitter_consumer_secret: str
    use_object_storage: bool
    use_star_for_reaction_fallback: bool
    email: str  # ayuskey or v11
    discord_client_id: str  # ayuskey or v11
    discord_client_secret: str  # ayuskey or v11
    drive_capacity_per_local_user_mb: int  # ayuskey or v11
    drive_capacity_per_remote_user_mb: int  # ayuskey or v11
    emojis: list[ICustomEmoji]  # v13から無くなった為
    background_image_url: str
    default_dark_theme: str
    default_light_theme: str
    email_required_for_signup: bool
    logo_image_url: str
    ads: list[IAds]  # v12 only
    translator_available: bool  # v12 only


class IInstancePolicies(TypedDict):
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


class IInstanceMetaRequired(IInstanceMetaLite):
    features: IInstanceFeatures
    cache_remote_files: bool


class IInstanceMeta(IInstanceMetaRequired, total=False):
    policies: IInstancePolicies
    pinned_pages: list[str]
    pinned_clip_id: str
    require_setup: bool
    proxy_account_name: str
