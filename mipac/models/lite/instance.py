from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.emoji import CustomEmoji
from mipac.types.ads import IAds
from mipac.types.instance import IInstanceLite, IInstanceMetaLite

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class LiteInstanceMeta:
    def __init__(
        self, instance: IInstanceMetaLite, *, client: ClientActions
    ) -> None:
        self.__instance: IInstanceMetaLite = instance
        self.__client: ClientActions = client

    @property
    def version(self) -> str:
        return self.__instance['version']

    @property
    def uri(self) -> str:
        return self.__instance['uri']

    @property
    def disable_registration(self) -> bool:
        return self.__instance['disable_registration']

    @property
    def disable_local_timeline(self) -> bool:
        return self.__instance['disable_local_timeline']

    @property
    def disable_global_timeline(self) -> bool:
        return self.__instance['disable_global_timeline']

    @property
    def drive_capacity_per_local_user_mb(self) -> int:
        return self.__instance['drive_capacity_per_local_user_mb']

    @property
    def drive_capacity_per_remote_user_mb(self) -> int:
        return self.__instance['drive_capacity_per_remote_user_mb']

    @property
    def enable_hcaptch(self) -> bool:
        return self.__instance['enable_hcaptcha']

    @property
    def max_note_text_length(self) -> int:
        return self.__instance['max_note_text_length']

    @property
    def enable_email(self) -> bool:
        return self.__instance['enable_email']

    @property
    def enable_twitter_integration(self) -> bool:
        return self.__instance['enable_twitter_integration']

    @property
    def enable_github_integration(self) -> bool:
        return self.__instance['enable_github_integration']

    @property
    def enable_discord_integration(self) -> bool:
        return self.__instance['enable_discord_integration']

    @property
    def enable_service_worker(self) -> bool:
        return self.__instance['enable_service_worker']

    @property
    def emojis(self) -> list[CustomEmoji]:
        return [
            CustomEmoji(i, client=self.__client)
            for i in self.__instance['emojis']
        ]

    @property
    def mascot_image_url(self) -> str:
        return self.__instance['mascot_image_url']

    @property
    def banner_url(self) -> str:
        return self.__instance['banner_url']

    @property
    def icon_url(self) -> str:
        return self.__instance['icon_url']

    @property
    def maintainer_name(self) -> str | None:
        return self.__instance.get('maintainer_name')

    @property
    def maintainer_email(self) -> str | None:
        return self.__instance.get('maintainer_email')

    @property
    def name(self) -> str | None:
        return self.__instance.get('name')

    @property
    def description(self) -> str | None:
        return self.__instance.get('description')

    @property
    def langs(self) -> list[str]:
        return self.__instance.get('langs', [])

    @property
    def tos_url(self) -> str | None:
        return self.__instance.get('tos_url')

    @property
    def tos_text_url(self) -> str | None:
        return self.__instance.get('tos_text_url')

    @property
    def announcements(self) -> dict[str, Any] | None:  # TODO: 型確認
        return self.__instance.get('announcements')

    @property
    def hcaptcha_site_key(self) -> str | None:
        return self.__instance.get('hcaptcha_site_key')

    @property
    def enable_recaptcha(self) -> bool:
        return self.__instance.get('enable_recaptcha', False)

    @property
    def recaptcha_siteKey(self) -> str | None:
        return self.__instance.get('recaptcha_siteKey')

    @property
    def sw_publickey(self) -> str | None:
        return self.__instance.get('sw_publickey')

    @property
    def ads(self) -> list[IAds] | None:  # TODO: モデルに
        return self.__instance.get('ads')


class LiteInstance:
    def __init__(self, instance: IInstanceLite) -> None:
        self.__instance: IInstanceLite = instance

    @property
    def name(self) -> str:
        return self.__instance['name']

    def software_name(self) -> str:
        return self.__instance['software_name']

    def software_version(self) -> str:
        return self.__instance['software_version']

    def icon_url(self) -> str:
        return self.__instance['icon_url']

    def favicon_url(self) -> str:
        return self.__instance['favicon_url']

    def theme_color(self) -> str:
        return self.__instance['theme_color']
