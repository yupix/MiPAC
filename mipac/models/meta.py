from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.meta import PartialMeta
from mipac.types.meta import (
    IAdminMeta,
    IFeatures,
    IMeta,
    ISensitiveMediaDetection,
    ISensitiveMediaDetectionSentivity,
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
    def hcaptcha(self) -> bool:
        return self.__raw_features["hcaptcha"]

    @property
    def recaptcha(self) -> bool:
        return self.__raw_features["recaptcha"]

    @property
    def turnstile(self) -> bool:
        return self.__raw_features["turnstile"]

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


class Meta(PartialMeta[IMeta]):
    def __init__(self, instance_metadata: IMeta, *, client: ClientManager) -> None:
        super().__init__(instance_metadata, client=client)

    @property
    def features(self) -> Features:
        return Features(self._raw_meta["features"])

    @property
    def cache_remote_files(self) -> bool:
        return self._raw_meta["cache_remote_files"]

    @property
    def cache_remote_sensitive_files(self) -> bool:
        return self._raw_meta["cache_remote_sensitive_files"]

    @property
    def require_setup(self) -> bool:
        return self._raw_meta["require_setup"]

    @property
    def proxy_account_name(self) -> str:
        return self._raw_meta["proxy_account_name"]


class AdminMeta:
    def __init__(self, raw_meta: IAdminMeta, *, client: ClientManager) -> None:
        self.__raw_meta: IAdminMeta = raw_meta
        self.__client: ClientManager = client

    @property
    def maintainer_name(self) -> str | None:
        return self.__raw_meta["maintainer_name"]

    @property
    def maintainer_email(self) -> str | None:
        return self.__raw_meta["maintainer_email"]

    @property
    def version(self) -> str:
        return self.__raw_meta["version"]

    @property
    def name(self) -> str | None:
        return self.__raw_meta["name"]

    @property
    def short_name(self) -> str | None:
        return self.__raw_meta["short_name"]

    @property
    def uri(self) -> str:
        return self.__raw_meta["uri"]

    @property
    def description(self) -> str | None:
        return self.__raw_meta["description"]

    @property
    def langs(self) -> list[str]:
        return self.__raw_meta["langs"]

    @property
    def tos_url(self) -> str:
        return self.__raw_meta["tos_url"]

    @property
    def repository_url(self) -> str:
        return self.__raw_meta["repository_url"]

    @property
    def feedback_url(self) -> str:
        return self.__raw_meta["feedback_url"]

    @property
    def disable_registration(self) -> bool:
        return self.__raw_meta["disable_registration"]

    @property
    def email_required_for_signup(self) -> bool:
        return self.__raw_meta["email_required_for_signup"]

    @property
    def enable_hcaptcha(self) -> bool:
        return self.__raw_meta["enable_hcaptcha"]

    @property
    def hcaptcha_site_key(self) -> str | None:
        return self.__raw_meta["hcaptcha_site_key"]

    @property
    def enable_recaptcha(self) -> bool:
        return self.__raw_meta["enable_recaptcha"]

    @property
    def recaptcha_site_key(self) -> str:
        return self.__raw_meta["recaptcha_site_key"]

    @property
    def enable_turnstile(self) -> bool:
        return self.__raw_meta["enable_turnstile"]

    @property
    def turnstile_site_key(self) -> str:
        return self.__raw_meta["turnstile_site_key"]

    @property
    def sw_publickey(self) -> str | None:
        return self.__raw_meta["sw_publickey"]

    @property
    def theme_color(self) -> str:
        return self.__raw_meta["theme_color"]

    @property
    def mascot_image_url(self) -> str:
        return self.__raw_meta["mascot_image_url"]

    @property
    def banner_url(self) -> str | None:
        return self.__raw_meta["banner_url"]

    @property
    def server_error_image_url(self) -> str | None:
        return self.__raw_meta["server_error_image_url"]

    @property
    def not_found_image_url(self) -> str | None:
        return self.__raw_meta["not_found_image_url"]

    @property
    def info_image_url(self) -> str | None:
        return self.__raw_meta["info_image_url"]

    @property
    def icon_url(self) -> str | None:
        return self.__raw_meta["icon_url"]

    @property
    def appint_icon_url(self) -> str | None:
        return self.__raw_meta["appint_icon_url"]

    @property
    def background_image_url(self) -> str | None:
        return self.__raw_meta["background_image_url"]

    @property
    def logo_image_url(self) -> str | None:
        return self.__raw_meta["logo_image_url"]

    @property
    def default_light_theme(self) -> str | None:
        return self.__raw_meta["default_light_theme"]

    @property
    def default_dark_theme(self) -> str | None:
        return self.__raw_meta["default_dark_theme"]

    @property
    def enable_email(self) -> bool:
        return self.__raw_meta["enable_email"]

    @property
    def enable_service_worker(self) -> bool:
        return self.__raw_meta["enable_service_worker"]

    @property
    def translator_available(self) -> bool:
        return self.__raw_meta["translator_available"]

    @property
    def cache_remote_files(self) -> bool:
        return self.__raw_meta["cache_remote_files"]

    @property
    def cache_remote_sensitive_files(self) -> bool:
        return self.__raw_meta["cache_remote_sensitive_files"]

    @property
    def pinned_users(self) -> list[str]:
        return self.__raw_meta["pinned_users"]

    @property
    def hidden_tags(self) -> list[str]:
        return self.__raw_meta["hidden_tags"]

    @property
    def blocked_hosts(self) -> list[str]:
        return self.__raw_meta["blocked_hosts"]

    @property
    def sensitive_words(self) -> list[str]:
        return self.__raw_meta["sensitive_words"]

    @property
    def preserved_usernames(self) -> list[str]:
        return self.__raw_meta["preserved_usernames"]

    @property
    def hcaptcha_secret_key(self) -> str | None:
        return self.__raw_meta["hcaptcha_secret_key"]

    @property
    def recaptcha_secret_key(self) -> str:
        return self.__raw_meta["recaptcha_secret_key"]

    @property
    def turnstile_secret_key(self) -> str:
        return self.__raw_meta["turnstile_secret_key"]

    @property
    def sensitive_media_detection(self) -> ISensitiveMediaDetection:
        return self.__raw_meta["sensitive_media_detection"]

    @property
    def sensitive_media_detection_sensitivity(self) -> ISensitiveMediaDetectionSentivity:
        return self.__raw_meta["sensitive_media_detection_sensitivity"]

    @property
    def set_sensitive_flag_automatically(self) -> bool:
        return self.__raw_meta["set_sensitive_flag_automatically"]

    @property
    def enable_sensitive_media_detection_for_videos(self) -> bool:
        return self.__raw_meta["enable_sensitive_media_detection_for_videos"]

    @property
    def proxy_account_id(self) -> str:
        return self.__raw_meta["proxy_account_id"]

    @property
    def summaly_proxy(self) -> str | None:
        return self.__raw_meta["summaly_proxy"]

    @property
    def email(self) -> str:
        return self.__raw_meta["email"]

    @property
    def smtp_secure(self) -> bool:
        return self.__raw_meta["smtp_secure"]

    @property
    def smtp_host(self) -> str:
        return self.__raw_meta["smtp_host"]

    @property
    def smtp_port(self) -> int:
        return self.__raw_meta["smtp_port"]

    @property
    def smtp_user(self) -> str:
        return self.__raw_meta["smtp_user"]

    @property
    def smtp_pass(self) -> str:
        return self.__raw_meta["smtp_pass"]

    @property
    def sw_private_key(self) -> str | None:
        return self.__raw_meta["sw_private_key"]

    @property
    def use_object_storage(self) -> bool:
        return self.__raw_meta["use_object_storage"]

    @property
    def object_storage_base_url(self) -> str:
        return self.__raw_meta["object_storage_base_url"]

    @property
    def object_storage_bucket(self) -> str:
        return self.__raw_meta["object_storage_bucket"]

    @property
    def object_storage_prefix(self) -> str:
        return self.__raw_meta["object_storage_prefix"]

    @property
    def object_storage_endpoint(self) -> str:
        return self.__raw_meta["object_storage_endpoint"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_meta.get(key)
