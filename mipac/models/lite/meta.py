from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from mipac.models.roles import RolePolicies
from mipac.types.ads import IAdPlaces
from mipac.types.meta import IPartialMeta

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.admins.ad import ClientAdminAdManager


class MetaAd:
    def __init__(self, raw_ad: Any, *, client: ClientManager) -> None:
        self._raw_ad: Any = raw_ad
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self._raw_ad["id"]

    @property
    def url(self) -> str:
        return self._raw_ad["url"]

    @property
    def place(self) -> IAdPlaces:
        return self._raw_ad["place"]

    @property
    def ratio(self) -> int:
        return self._raw_ad["ratio"]

    @property
    def image_url(self) -> str:
        return self._raw_ad["image_url"]

    @property
    def day_of_week(self) -> int:
        return self._raw_ad["day_of_week"]

    @property
    def is_sensitive(self) -> bool:
        return self._raw_ad["is_sensitive"]

    @property
    def api(self) -> ClientAdminAdManager:
        return self.__client.admin._create_client_ad_manager(ad_id=self.id)

    def _get(self, key: str) -> Any | None:
        """You can access the raw response data directly by specifying the key

        Returns
        -------
        Any | None
            raw response data
        """
        return self._raw_ad.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, MetaAd) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class PartialMeta[T: IPartialMeta]:
    def __init__(self, raw_meta: T, *, client: ClientManager) -> None:
        self._raw_meta: T = raw_meta
        self.__client: ClientManager = client

    @property
    def maintainer_name(self) -> str | None:
        return self._raw_meta["maintainer_name"]

    @property
    def maintainer_email(self) -> str | None:
        return self._raw_meta["maintainer_email"]

    @property
    def version(self) -> str:
        return self._raw_meta["version"]

    @property
    def name(self) -> str | None:
        return self._raw_meta["name"]

    @property
    def short_name(self) -> str | None:
        return self._raw_meta["short_name"]

    @property
    def uri(self) -> str:
        return self._raw_meta["uri"]

    @property
    def description(self) -> str | None:
        return self._raw_meta["description"]

    @property
    def langs(self) -> list[str]:
        return self._raw_meta["langs"]

    @property
    def tos_url(self) -> str | None:
        return self._raw_meta["tos_url"]

    @property
    def repository_url(self) -> str | None:
        return self._raw_meta["repository_url"]

    @property
    def feedback_url(self) -> str | None:
        return self._raw_meta["feedback_url"]

    @property
    def default_dark_theme(self) -> str | None:
        return self._raw_meta["default_dark_theme"]

    @property
    def default_light_theme(self) -> str | None:
        return self._raw_meta["default_light_theme"]

    @property
    def disable_registration(self) -> bool:
        return self._raw_meta["disable_registration"]

    @property
    def email_required_for_signup(self) -> bool:
        return self._raw_meta["email_required_for_signup"]

    @property
    def enable_hcaptcha(self) -> bool:
        return self._raw_meta["enable_hcaptcha"]

    @property
    def hcaptcha_site_key(self) -> str | None:
        return self._raw_meta["hcaptcha_site_key"]

    @property
    def enable_mcaptcha(self) -> bool:
        return self._raw_meta["enable_mcaptcha"]

    @property
    def mcaptcha_site_key(self) -> str | None:
        return self._raw_meta["mcaptcha_site_key"]

    @property
    def mcaptcha_instance_url(self) -> str | None:
        return self._raw_meta["mcaptcha_instance_url"]

    @property
    def enable_recaptcha(self) -> bool:
        return self._raw_meta["enable_recaptcha"]

    @property
    def recaptcha_site_key(self) -> str | None:
        return self._raw_meta["recaptcha_site_key"]

    @property
    def enable_turnstile(self) -> bool:
        return self._raw_meta["enable_turnstile"]

    @property
    def turnstile_site_key(self) -> str | None:
        return self._raw_meta["turnstile_site_key"]

    @property
    def enable_testcaptcha(self) -> bool:
        return self._raw_meta["enable_testcaptcha"]

    @property
    def sw_publickey(self) -> str | None:
        return self._raw_meta["sw_publickey"]

    @property
    def mascot_image_url(self) -> str:
        return self._raw_meta["mascot_image_url"]

    @property
    def banner_url(self) -> str | None:
        return self._raw_meta["banner_url"]

    @property
    def server_error_image_url(self) -> str | None:
        return self._raw_meta["server_error_image_url"]

    @property
    def info_image_url(self) -> str | None:
        return self._raw_meta["info_image_url"]

    @property
    def not_found_image_url(self) -> str | None:
        return self._raw_meta["not_found_image_url"]

    @property
    def icon_url(self) -> str | None:
        return self._raw_meta["icon_url"]

    @property
    def max_note_text_length(self) -> int:
        return self._raw_meta["max_note_text_length"]

    @property
    def ads(self) -> list[MetaAd]:
        return [MetaAd(raw_ad, client=self.__client) for raw_ad in self._raw_meta["ads"]]

    @property
    def notes_per_one_ad(self) -> int:
        return self._raw_meta["notes_per_one_ad"]

    @property
    def enable_email(self) -> bool:
        return self._raw_meta["enable_email"]

    @property
    def enable_service_worker(self) -> bool:
        return self._raw_meta["enable_service_worker"]

    @property
    def translator_available(self) -> bool:
        return self._raw_meta["translator_available"]

    @property
    def media_proxy(self) -> bool:
        return self._raw_meta["media_proxy"]

    @property
    def enable_url_preview(self) -> bool:
        return self._raw_meta["enable_url_preview"]

    @property
    def background_image_url(self) -> str | None:
        return self._raw_meta["background_image_url"]

    @property
    def impressum_url(self) -> bool:
        return self._raw_meta["impressum_url"]

    @property
    def logo_image_url(self) -> bool:
        return self._raw_meta["logo_image_url"]

    @property
    def privacy_policy_url(self) -> bool:
        return self._raw_meta["privacy_policy_url"]

    @property
    def inquiry_url(self) -> bool:
        return self._raw_meta["inquiry_url"]

    @property
    def server_rules(self) -> list[str]:
        return self._raw_meta["server_rules"]

    @property
    def theme_color(self) -> str:
        return self._raw_meta["theme_color"]

    @property
    def policies(self) -> RolePolicies:
        return RolePolicies(self._raw_meta["policies"])

    @property
    def note_searchable_scope(self) -> Literal["local", "global"]:
        return self._raw_meta["note_searchable_scope"]

    @property
    def max_file_size(self) -> int:
        return self._raw_meta["max_file_size"]

    def _get(self, key: str) -> Any | None:
        return self._raw_meta.get(key)
