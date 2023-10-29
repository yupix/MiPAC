from typing import Any, Literal, NotRequired, TypedDict

from mipac.types.ads import IPartialAd

ISensitiveMediaDetectionSentivity = Literal["medium", "low", "high", "veryLow", "veryHigh"]
ISensitiveMediaDetection = Literal["none", "all", "local", "remote"]


class IFeatures(TypedDict):
    registration: bool
    email_required_for_signup: bool
    hcaptcha: bool
    recaptcha: bool
    turnstile: bool
    object_storage: bool
    service_worker: bool
    miauth: bool


class IPolicies(TypedDict):
    gtl_available: bool
    ltl_available: bool
    can_public_note: bool
    can_edit_note: bool
    can_invite: bool
    invite_limit: int
    invite_limit_cycle: int
    invite_expiration_time: int
    can_manage_custom_emojis: bool
    can_search_notes: bool
    can_use_translator: bool
    can_hide_ads: bool
    drive_capacity_mb: int
    always_mark_nsfw: bool
    pin_limit: int
    antenna_limit: int
    word_mute_limit: int
    webhook_limit: int
    clip_limit: int
    note_each_clips_limit: int
    user_list_limit: int
    user_each_user_lists_limit: int
    rate_limit_factor: int


class IPartialMeta(TypedDict):
    maintainer_name: str | None
    maintainer_email: str | None
    version: str
    name: None
    short_name: None
    uri: str
    description: None
    langs: list[str]
    tos_url: str
    repository_url: str
    feedback_url: str
    disable_registration: bool
    email_required_for_signup: bool
    enable_hcaptcha: bool
    hcaptcha_site_key: None
    enable_recaptcha: bool
    recaptcha_site_key: str
    enable_turnstile: bool
    turnstile_site_key: str
    sw_publickey: None
    theme_color: str
    mascot_image_url: str
    banner_url: str | None
    info_image_url: str | None
    server_error_image_url: str | None
    not_found_image_url: str | None
    icon_url: str | None
    background_image_url: str | None
    logo_image_url: str | None
    max_note_text_length: int
    default_light_theme: str | None
    default_dark_theme: str | None
    ads: list[IPartialAd]
    enable_email: bool
    enable_service_worker: bool
    translator_available: bool
    server_rules: list[str]
    policies: IPolicies
    media_proxy: str


class IMeta(IPartialMeta):
    features: IFeatures
    cache_remote_files: bool
    cache_remote_sensitive_files: bool
    require_setup: bool
    proxy_account_name: str


class IAdminMeta(TypedDict):  # IMetaに含まれる物が多くあるけど、ない場合もあるので別にする
    maintainer_name: str | None
    maintainer_email: str | None
    version: str
    name: str | None
    short_name: str | None
    uri: str
    description: str | None
    langs: list[str]
    tos_url: str
    repository_url: str
    feedback_url: str
    disable_registration: bool
    email_required_for_signup: bool
    enable_hcaptcha: bool
    hcaptcha_site_key: str | None
    enable_recaptcha: bool
    recaptcha_site_key: str
    enable_turnstile: bool
    turnstile_site_key: str
    sw_publickey: str | None
    theme_color: str
    mascot_image_url: str
    banner_url: str | None
    server_error_image_url: str | None
    not_found_image_url: str | None
    info_image_url: str | None
    icon_url: str | None
    appint_icon_url: str | None
    appint_icon_url: str | None
    background_image_url: str | None
    logo_image_url: str | None
    default_light_theme: str | None
    default_dark_theme: str | None
    enable_email: bool
    enable_service_worker: bool
    translator_available: bool
    cache_remote_files: bool
    cache_remote_sensitive_files: bool
    pinned_users: list[str]
    hidden_tags: list[str]
    blocked_hosts: list[str]
    sensitive_words: list[str]
    preserved_usernames: list[str]
    hcaptcha_secret_key: str | None
    recaptcha_secret_key: str
    turnstile_secret_key: str
    sensitive_media_detection: ISensitiveMediaDetection
    sensitive_media_detection_sensitivity: ISensitiveMediaDetectionSentivity
    set_sensitive_flag_automatically: bool
    enable_sensitive_media_detection_for_videos: bool
    proxy_account_id: str
    summaly_proxy: str | None
    email: str
    smtp_secure: bool
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    sw_private_key: str | None
    use_object_storage: bool
    object_storage_base_url: str
    object_storage_bucket: str
    object_storage_prefix: str
    object_storage_endpoint: str
    object_storage_region: str
    object_storage_port: str | None
    object_storage_access_key: str
    object_storage_secret_key: str
    object_storage_use_s_s_l: bool
    object_storage_use_proxy: bool
    object_storage_set_public_read: bool
    object_storage_sint_force_path_style: bool
    deepl_auth_key: str | None
    deepl_is_pro: bool
    enable_ip_logging: bool
    enable_active_email_validation: bool
    enable_charts_for_remote_user: bool
    enable_charts_for_federated_instances: bool
    enable_server_machine_stats: bool
    enable_identicon_generation: bool
    policies: IPolicies
    manifest_json_override: dict[str, Any]


class IUpdateMetaBody(TypedDict, total=False):
    announcements: list
    disable_registration: bool
    disable_local_timeline: bool
    disable_global_timeline: bool
    enable_emoji_reaction: bool
    use_star_for_reaction_fallback: bool
    pinned_users: list[str]
    hidden_tags: list[str]
    blocked_hosts: list[str]
    mascot_image_url: str | None
    banner_url: str | None
    error_image_url: str | None
    icon_url: str | None
    name: str | None
    description: str | None
    max_note_text_length: int
    local_drive_capacity_mb: int
    remote_drive_capacity_mb: int
    cache_remote_files: bool
    proxy_remote_files: bool
    enable_recaptcha: bool
    recaptcha_site_key: str
    recaptcha_secret_key: str
    enable_turnstile: bool
    turnstile_site_key: str
    turnstile_secret_key: str
    proxy_account_id: str | None
    proxy_account: str
    maintainer_name: str | None
    maintainer_email: str | None
    langs: str
    summaly_proxy: str | None
    enable_twitter_integration: bool
    twitter_consumer_key: str | None
    twitter_consumer_secret: str | None
    enable_github_integration: bool
    github_client_id: str | None
    github_client_secret: str | None
    enable_discord_integration: bool
    discord_client_id: str | None
    discord_client_secret: str | None
    enable_email: bool
    email: str
    smtp_secure: bool
    smtp_host: str | None
    smtp_port: int | None
    smtp_user: str | None
    smtp_pass: str | None
    enable_service_worker: bool
    sw_public_key: str
    sw_private_key: str
    tos_url: str | None
    tos_text_url: str
    repository_url: str
    feedback_url: str
    use_object_storage: bool
    object_storage_base_url: str | None
    object_storage_bucket: str | None
    object_storage_prefix: str | None
    object_storage_endpoint: str | None
    object_storage_region: str | None
    object_storage_port: int | None
    object_storage_access_key: str | None
    object_storage_secret_key: str | None
    object_storage_use_s_s_l: bool
    object_storage_use_proxy: bool
    object_storage_set_public_read: bool
    object_storage_s3_force_path_style: bool
    server_rules: NotRequired[
        list[str]
    ]  # v13.11.3以降のバージョンから追加。その場合は使わないとエラー出るかも
