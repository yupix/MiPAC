from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.ad import PartialAd
from mipac.types.meta import IPartialMeta, IPolicies

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Policies:
    def __init__(self, raw_policies: IPolicies) -> None:
        self.__raw_policies: IPolicies = raw_policies

    @property
    def gtl_available(self) -> bool:
        """Whether GTL is effective"""
        return self.__raw_policies["gtl_available"]

    @property
    def ltl_available(self) -> bool:
        """Whether LTL is effective"""
        return self.__raw_policies["ltl_available"]

    @property
    def can_public_note(self) -> bool:
        """Whether you can post a public note"""
        return self.__raw_policies["can_public_note"]

    @property
    def can_edit_note(self) -> bool:
        """Whether you can edit a note"""
        return self.__raw_policies["can_edit_note"]

    @property
    def can_invite(self) -> bool:
        """Whether you can invite"""
        return self.__raw_policies["can_invite"]

    @property
    def invite_limit(self) -> int:
        return self.__raw_policies["invite_limit"]

    @property
    def invite_limit_cycle(self) -> int:
        return self.__raw_policies["invite_limit_cycle"]

    @property
    def invite_expiration_time(self) -> int:
        return self.__raw_policies["invite_expiration_time"]

    @property
    def can_manage_custom_emojis(self) -> bool:
        """Whether you can manage custom emojis"""
        return self.__raw_policies["can_manage_custom_emojis"]

    @property
    def can_search_notes(self) -> bool:
        """Whether you can search note"""
        return self.__raw_policies["can_search_notes"]

    @property
    def can_use_translator(self) -> bool:
        """Whether you can use translator"""
        return self.__raw_policies["can_use_translator"]

    @property
    def can_hide_ads(self) -> bool:
        """Whether you can hide ads"""
        return self.__raw_policies["can_hide_ads"]

    @property
    def drive_capacity_mb(self) -> int:
        return self.__raw_policies["drive_capacity_mb"]

    @property
    def always_mark_nsfw(self) -> bool:
        return self.__raw_policies["always_mark_nsfw"]

    @property
    def pin_limit(self) -> int:
        return self.__raw_policies["pin_limit"]

    @property
    def antenna_limit(self) -> int:
        return self.__raw_policies["antenna_limit"]

    @property
    def word_mute_limit(self) -> int:
        return self.__raw_policies["word_mute_limit"]

    @property
    def webhook_limit(self) -> int:
        return self.__raw_policies["webhook_limit"]

    @property
    def clip_limit(self) -> int:
        return self.__raw_policies["clip_limit"]

    @property
    def note_each_clips_limit(self) -> int:
        return self.__raw_policies["note_each_clips_limit"]

    @property
    def user_list_limit(self) -> int:
        return self.__raw_policies["user_list_limit"]

    @property
    def user_each_user_lists_limit(self) -> int:
        return self.__raw_policies["user_each_user_lists_limit"]

    @property
    def rate_limit_factor(self) -> int:
        return self.__raw_policies["rate_limit_factor"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_policies.get(key)


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
    def tos_url(self) -> str:
        return self._raw_meta["tos_url"]

    @property
    def repository_url(self) -> str:
        return self._raw_meta["repository_url"]

    @property
    def feedback_url(self) -> str:
        return self._raw_meta["feedback_url"]

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
    def enable_recaptcha(self) -> bool:
        return self._raw_meta["enable_recaptcha"]

    @property
    def recaptcha_site_key(self) -> str:
        return self._raw_meta["recaptcha_site_key"]

    @property
    def enable_turnstile(self) -> bool:
        return self._raw_meta["enable_turnstile"]

    @property
    def turnstile_site_key(self) -> str:
        return self._raw_meta["turnstile_site_key"]

    @property
    def sw_publickey(self) -> str | None:
        return self._raw_meta["sw_publickey"]

    @property
    def theme_color(self) -> str:
        return self._raw_meta["theme_color"]

    @property
    def mascot_image_url(self) -> str:
        return self._raw_meta["mascot_image_url"]

    @property
    def banner_url(self) -> str | None:
        return self._raw_meta["banner_url"]

    @property
    def info_image_url(self) -> str | None:
        return self._raw_meta["info_image_url"]

    @property
    def server_error_image_url(self) -> str | None:
        return self._raw_meta["server_error_image_url"]

    @property
    def not_found_image_url(self) -> str | None:
        return self._raw_meta["not_found_image_url"]

    @property
    def icon_url(self) -> str | None:
        return self._raw_meta["icon_url"]

    @property
    def background_image_url(self) -> str | None:
        return self._raw_meta["background_image_url"]

    @property
    def logo_image_url(self) -> str | None:
        return self._raw_meta["logo_image_url"]

    @property
    def max_note_text_length(self) -> int:
        return self._raw_meta["max_note_text_length"]

    @property
    def default_light_theme(self) -> str | None:
        return self._raw_meta["default_light_theme"]

    @property
    def default_dark_theme(self) -> str | None:
        return self._raw_meta["default_dark_theme"]

    @property
    def ads(self) -> list[PartialAd]:
        return [PartialAd(raw_ad, client=self.__client) for raw_ad in self._raw_meta["ads"]]

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
    def server_rules(self) -> list[str]:
        return self._raw_meta["server_rules"]

    @property
    def policies(self) -> IPolicies:
        return self._raw_meta["policies"]

    @property
    def media_proxy(self) -> str:
        return self._raw_meta["media_proxy"]

    def _get(self, key: str) -> Any | None:
        return self._raw_meta.get(key)
