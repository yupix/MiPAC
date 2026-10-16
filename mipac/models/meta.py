from __future__ import annotations


from typing import TYPE_CHECKING, Any

from mipac.models.lite.meta import PartialMeta
from mipac.types.meta import (
    IAdminMeta,
    IFeatures,
    IMetaDetailed,
    IMetaDetailedOnly,
)

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Features:
    def __init__(self, raw_features: IFeatures) -> None:
        self.__raw_features = raw_features

    @property
    def registration(self) -> bool:
        return self.__raw_features["registration"]

    @property
    def email_required_for_signup(self) -> bool:
        return self.__raw_features["email_required_for_signup"]

    @property
    def local_timeline(self) -> bool:
        return self.__raw_features["local_timeline"]

    @property
    def global_timeline(self) -> bool:
        return self.__raw_features["global_timeline"]

    @property
    def hcaptcha(self) -> bool:
        return self.__raw_features["hcaptcha"]

    @property
    def turnstile(self) -> bool:
        return self.__raw_features["turnstile"]

    @property
    def recaptcha(self) -> bool:
        return self.__raw_features["recaptcha"]

    @property
    def object_storage(self) -> bool:
        return self.__raw_features["object_storage"]

    @property
    def service_worker(self) -> bool:
        return self.__raw_features["service_worker"]

    @property
    def miauth(self) -> bool:
        return self.__raw_features["miauth"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_features.get(key)


class MetaDetailedOnly:
    def __init__(self, raw_meta: IMetaDetailedOnly, *, client: ClientManager):
        self._raw_meta: IMetaDetailedOnly = raw_meta

    @property
    def features(self) -> Features:
        return Features(self._raw_meta["features"])

    @property
    def proxy_account_name(self) -> str | None:
        return self._raw_meta["proxy_account_name"]

    @property
    def require_setup(self) -> bool:
        return self._raw_meta["require_setup"]

    @property
    def cache_remote_files(self) -> bool:
        return self._raw_meta["cache_remote_files"]

    @property
    def cache_remote_sensitive_files(self) -> bool:
        return self._raw_meta["cache_remote_sensitive_files"]


class Meta(PartialMeta[IMetaDetailed], MetaDetailedOnly):
    def __init__(self, instance_metadata: IMetaDetailed, *, client: ClientManager) -> None:
        super().__init__(instance_metadata, client=client)


class AdminMeta:
    def __init__(self, raw_admin_meta: IAdminMeta, *, client: ClientManager) -> None:
        self.__raw_admin_meta: IAdminMeta = raw_admin_meta
        self.__client: ClientManager = client

    @property
    def cache_remote_files(self):
        return self.__raw_admin_meta["cache_remote_files"]

    @property
    def cache_remote_sensitive_files(self):
        return self.__raw_admin_meta["cache_remote_sensitive_files"]

    @property
    def email_required_for_signup(self):
        return self.__raw_admin_meta["email_required_for_signup"]

    @property
    def enable_hcaptcha(self):
        return self.__raw_admin_meta["enable_hcaptcha"]

    @property
    def hcaptcha_site_key(self):
        return self.__raw_admin_meta["hcaptcha_site_key"]

    @property
    def enable_mcaptcha(self):
        return self.__raw_admin_meta["enable_mcaptcha"]

    @property
    def mcaptcha_site_key(self):
        return self.__raw_admin_meta["mcaptcha_site_key"]

    @property
    def mcaptcha_instance_url(self):
        return self.__raw_admin_meta["mcaptcha_instance_url"]

    @property
    def enable_recaptcha(self):
        return self.__raw_admin_meta["enable_recaptcha"]

    @property
    def recaptcha_site_key(self):
        return self.__raw_admin_meta["recaptcha_site_key"]

    @property
    def enable_turnstile(self):
        return self.__raw_admin_meta["enable_turnstile"]

    @property
    def turnstile_site_key(self):
        return self.__raw_admin_meta["turnstile_site_key"]

    @property
    def enable_testcaptcha(self):
        return self.__raw_admin_meta["enable_testcaptcha"]

    @property
    def sw_publickey(self):
        return self.__raw_admin_meta["sw_publickey"]

    @property
    def mascot_image_url(self):
        return self.__raw_admin_meta["mascot_image_url"]

    @property
    def banner_url(self):
        return self.__raw_admin_meta["banner_url"]

    @property
    def server_error_image_url(self):
        return self.__raw_admin_meta["server_error_image_url"]

    @property
    def info_image_url(self):
        return self.__raw_admin_meta["info_image_url"]

    @property
    def not_found_image_url(self):
        return self.__raw_admin_meta["not_found_image_url"]

    @property
    def icon_url(self):
        return self.__raw_admin_meta["icon_url"]

    @property
    def app192_icon_url(self):
        return self.__raw_admin_meta["app192_icon_url"]

    @property
    def app512_icon_url(self):
        return self.__raw_admin_meta["app512_icon_url"]

    @property
    def enable_email(self):
        return self.__raw_admin_meta["enable_email"]

    @property
    def enable_service_worker(self):
        return self.__raw_admin_meta["enable_service_worker"]

    @property
    def translator_available(self):
        return self.__raw_admin_meta["translator_available"]

    @property
    def silenced_hosts(self):
        return self.__raw_admin_meta.get("silenced_hosts")

    @property
    def media_silenced_hosts(self):
        return self.__raw_admin_meta["media_silenced_hosts"]

    @property
    def pinned_users(self):
        return self.__raw_admin_meta["pinned_users"]

    @property
    def hidden_tags(self):
        return self.__raw_admin_meta["hidden_tags"]

    @property
    def blocked_hosts(self):
        return self.__raw_admin_meta["blocked_hosts"]

    @property
    def sensitive_words(self):
        return self.__raw_admin_meta["sensitive_words"]

    @property
    def prohibited_words(self):
        return self.__raw_admin_meta["prohibited_words"]

    @property
    def prohibited_words_for_name_of_user(self):
        return self.__raw_admin_meta["prohibited_words_for_name_of_user"]

    @property
    def banned_email_domains(self):
        return self.__raw_admin_meta.get("banned_email_domains")

    @property
    def preserved_usernames(self):
        return self.__raw_admin_meta["preserved_usernames"]

    @property
    def hcaptcha_secret_key(self):
        return self.__raw_admin_meta["hcaptcha_secret_key"]

    @property
    def mcaptcha_secret_key(self):
        return self.__raw_admin_meta["mcaptcha_secret_key"]

    @property
    def recaptcha_secret_key(self):
        return self.__raw_admin_meta["recaptcha_secret_key"]

    @property
    def turnstile_secret_key(self):
        return self.__raw_admin_meta["turnstile_secret_key"]

    @property
    def sensitive_media_detection(self):
        return self.__raw_admin_meta["sensitive_media_detection"]

    @property
    def sensitive_media_detection_sensitivity(self):
        return self.__raw_admin_meta["sensitive_media_detection_sensitivity"]

    @property
    def set_sensitive_flag_automatically(self):
        return self.__raw_admin_meta["set_sensitive_flag_automatically"]

    @property
    def enable_sensitive_media_detection_for_videos(self):
        return self.__raw_admin_meta["enable_sensitive_media_detection_for_videos"]

    @property
    def proxy_account_id(self):
        return self.__raw_admin_meta["proxy_account_id"]

    @property
    def email(self):
        return self.__raw_admin_meta["email"]

    @property
    def smtp_secure(self):
        return self.__raw_admin_meta["smtp_secure"]

    @property
    def smtp_host(self):
        return self.__raw_admin_meta["smtp_host"]

    @property
    def smtp_port(self):
        return self.__raw_admin_meta["smtp_port"]

    @property
    def smtp_user(self):
        return self.__raw_admin_meta["smtp_user"]

    @property
    def smtp_pass(self):
        return self.__raw_admin_meta["smtp_pass"]

    @property
    def sw_private_key(self):
        return self.__raw_admin_meta["sw_private_key"]

    @property
    def use_object_storage(self):
        return self.__raw_admin_meta["use_object_storage"]

    @property
    def object_storage_base_url(self):
        return self.__raw_admin_meta["object_storage_base_url"]

    @property
    def object_storage_bucket(self):
        return self.__raw_admin_meta["object_storage_bucket"]

    @property
    def object_storage_prefix(self):
        return self.__raw_admin_meta["object_storage_prefix"]

    @property
    def object_storage_endpoint(self):
        return self.__raw_admin_meta["object_storage_endpoint"]

    @property
    def object_storage_region(self):
        return self.__raw_admin_meta["object_storage_region"]

    @property
    def object_storage_port(self):
        return self.__raw_admin_meta["object_storage_port"]

    @property
    def object_storage_access_key(self):
        return self.__raw_admin_meta["object_storage_access_key"]

    @property
    def object_storage_secret_key(self):
        return self.__raw_admin_meta["object_storage_secret_key"]

    @property
    def object_storage_use_ssl(self):
        return self.__raw_admin_meta["object_storage_use_ssl"]

    @property
    def object_storage_use_proxy(self):
        return self.__raw_admin_meta["object_storage_use_proxy"]

    @property
    def object_storage_set_public_read(self):
        return self.__raw_admin_meta["object_storage_set_public_read"]

    @property
    def enable_ip_logging(self):
        return self.__raw_admin_meta["enable_ip_logging"]

    @property
    def enable_active_email_validation(self):
        return self.__raw_admin_meta["enable_active_email_validation"]

    @property
    def enable_verifymail_api(self):
        return self.__raw_admin_meta["enable_verifymail_api"]

    @property
    def verifymail_auth_key(self):
        return self.__raw_admin_meta["verifymail_auth_key"]

    @property
    def enable_truemail_api(self):
        return self.__raw_admin_meta["enable_truemail_api"]

    @property
    def truemail_instance(self):
        return self.__raw_admin_meta["truemail_instance"]

    @property
    def truemail_auth_key(self):
        return self.__raw_admin_meta["truemail_auth_key"]

    @property
    def enable_charts_for_remote_user(self):
        return self.__raw_admin_meta["enable_charts_for_remote_user"]

    @property
    def enable_charts_for_federated_instances(self):
        return self.__raw_admin_meta["enable_charts_for_federated_instances"]

    @property
    def enable_stats_for_federated_instances(self):
        return self.__raw_admin_meta["enable_stats_for_federated_instances"]

    @property
    def enable_server_machine_stats(self):
        return self.__raw_admin_meta["enable_server_machine_stats"]

    @property
    def enable_identicon_generation(self):
        return self.__raw_admin_meta["enable_identicon_generation"]

    @property
    def manifest_json_override(self):
        return self.__raw_admin_meta["manifest_json_override"]

    @property
    def policies(self):
        return self.__raw_admin_meta["policies"]

    @property
    def enable_fanout_timeline(self):
        return self.__raw_admin_meta["enable_fanout_timeline"]

    @property
    def enable_fanout_timeline_db_fallback(self):
        return self.__raw_admin_meta["enable_fanout_timeline_db_fallback"]

    @property
    def per_local_user_user_timeline_cache_max(self):
        return self.__raw_admin_meta["per_local_user_user_timeline_cache_max"]

    @property
    def per_remote_user_user_timeline_cache_max(self):
        return self.__raw_admin_meta["per_remote_user_user_timeline_cache_max"]

    @property
    def per_user_home_timeline_cache_max(self):
        return self.__raw_admin_meta["per_user_home_timeline_cache_max"]

    @property
    def per_user_list_timeline_cache_max(self):
        return self.__raw_admin_meta["per_user_list_timeline_cache_max"]

    @property
    def enable_reactions_buffering(self):
        return self.__raw_admin_meta["enable_reactions_buffering"]

    @property
    def notes_per_one_ad(self):
        return self.__raw_admin_meta["notes_per_one_ad"]

    @property
    def background_image_url(self):
        return self.__raw_admin_meta["background_image_url"]

    @property
    def deepl_auth_key(self):
        return self.__raw_admin_meta["deepl_auth_key"]

    @property
    def deepl_is_pro(self):
        return self.__raw_admin_meta["deepl_is_pro"]

    @property
    def default_dark_theme(self):
        return self.__raw_admin_meta["default_dark_theme"]

    @property
    def default_light_theme(self):
        return self.__raw_admin_meta["default_light_theme"]

    @property
    def description(self):
        return self.__raw_admin_meta["description"]

    @property
    def disable_registration(self):
        return self.__raw_admin_meta["disable_registration"]

    @property
    def impressum_url(self):
        return self.__raw_admin_meta["impressum_url"]

    @property
    def maintainer_email(self):
        return self.__raw_admin_meta["maintainer_email"]

    @property
    def maintainer_name(self):
        return self.__raw_admin_meta["maintainer_name"]

    @property
    def name(self):
        return self.__raw_admin_meta["name"]

    @property
    def short_name(self):
        return self.__raw_admin_meta["short_name"]

    @property
    def object_storage_s3_force_path_style(self):
        return self.__raw_admin_meta["object_storage_s3_force_path_style"]

    @property
    def privacy_policy_url(self):
        return self.__raw_admin_meta["privacy_policy_url"]

    @property
    def inquiry_url(self):
        return self.__raw_admin_meta["inquiry_url"]

    @property
    def repository_url(self):
        return self.__raw_admin_meta["repository_url"]

    @property
    def summaly_proxy(self):
        return self.__raw_admin_meta["summaly_proxy"]

    @property
    def theme_color(self):
        return self.__raw_admin_meta["theme_color"]

    @property
    def tos_url(self):
        return self.__raw_admin_meta["tos_url"]

    @property
    def uri(self):
        return self.__raw_admin_meta["uri"]

    @property
    def version(self):
        return self.__raw_admin_meta["version"]

    @property
    def url_preview_enabled(self):
        return self.__raw_admin_meta["url_preview_enabled"]

    @property
    def url_preview_timeout(self):
        return self.__raw_admin_meta["url_preview_timeout"]

    @property
    def url_preview_maximum_content_length(self):
        return self.__raw_admin_meta["url_preview_maximum_content_length"]

    @property
    def url_preview_require_content_length(self):
        return self.__raw_admin_meta["url_preview_require_content_length"]

    @property
    def url_preview_user_agent(self):
        return self.__raw_admin_meta["url_preview_user_agent"]

    @property
    def url_preview_summary_proxy_url(self):
        return self.__raw_admin_meta["url_preview_summary_proxy_url"]

    @property
    def federation(self):
        return self.__raw_admin_meta["federation"]

    @property
    def federation_hosts(self):
        return self.__raw_admin_meta["federation_hosts"]

    @property
    def sensitive_media_detection_api_url(self):
        return self.__raw_admin_meta["sensitive_media_detection_api_url"]

    @property
    def sensitive_media_detection_api_key(self):
        return self.__raw_admin_meta["sensitive_media_detection_api_key"]

    @property
    def sensitive_media_detection_timeout(self):
        return self.__raw_admin_meta["sensitive_media_detection_timeout"]

    @property
    def sensitive_media_detection_max_images_per_request(self):
        return self.__raw_admin_meta["sensitive_media_detection_max_images_per_request"]

    @property
    def url_preview_sensitive_list(self):
        return self.__raw_admin_meta["url_preview_sensitive_list"]

    @property
    def show_role_badges_of_remote_users(self):
        return self.__raw_admin_meta["show_role_badges_of_remote_users"]

    @property
    def client_options(self):
        return self.__raw_admin_meta["client_options"]
