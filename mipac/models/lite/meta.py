from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.models.emoji import CustomEmoji
from mipac.types.ads import IAds

from mipac.types.meta import (
    ICPU,
    IAnnouncement,
    ILiteMeta,
    IMetaCommon,
)

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class CPU:
    def __init__(self, cpu: ICPU) -> None:
        self.__cpu: ICPU = cpu

    @property
    def cores(self) -> int:
        return self.__cpu['cores']

    @property
    def model(self) -> str:
        return self.__cpu['model']


class MetaCommon:
    def __init__(
        self, meta_common: IMetaCommon, *, client: ClientManager
    ) -> None:
        self.__meta_common: IMetaCommon = meta_common
        self.__client = client

    @property
    def cache_remote_files(self) -> bool:
        return self.__meta_common['cache_remote_files']

    @property
    def enable_hcaptch(self) -> bool:
        return self.__meta_common['enable_hcaptch']

    @property
    def hcaptcha_site_key(self) -> str | None:
        return self.__meta_common['hcaptcha_site_key']

    @property
    def enable_recaptcha(self) -> bool:
        return self.__meta_common['enable_recaptcha']

    @property
    def recaptcha_site_key(self) -> str:
        return self.__meta_common['recaptcha_site_key']

    @property
    def sw_publickey(self) -> str | None:
        return self.__meta_common['sw_publickey']

    @property
    def banner_url(self) -> str | None:
        return self.__meta_common['banner_url']

    @property
    def error_image_url(self) -> str | None:
        return self.__meta_common['error_image_url']

    @property
    def icon_url(self) -> str | None:
        return self.__meta_common['icon_url']

    @property
    def max_note_text_length(self) -> int:
        return self.__meta_common['max_note_text_length']

    @property
    def enable_email(self) -> bool:
        return self.__meta_common['enable_email']

    @property
    def enable_twitter_integration(self) -> bool:
        return self.__meta_common['enable_twitter_integration']

    @property
    def enable_github_integration(self) -> bool:
        return self.__meta_common['enable_github_integration']

    @property
    def enable_discord_integration(self) -> bool:
        return self.__meta_common['enable_discord_integration']

    @property
    def enable_service_worker(self) -> bool:
        return self.__meta_common['enable_service_worker']

    @property
    def proxy_account_name(self) -> str | None:
        return self.__meta_common['proxy_account_name']

    @property
    def use_star_for_reaction_fallback(self) -> bool:
        return self.__meta_common.get('use_star_for_reaction_fallback', False)

    @property
    def object_storage_s3_force_path_style(self) -> bool:
        """
        objectStorageでs3ForcePathStyleを使用するかどうか
        注意: v11の管理者のみ取得できます

        Returns
        -------
        bool
            有効かどうか
        """
        return self.__meta_common.get(
            'object_storage_s3_force_path_style', False
        )

    # v12 only

    @property
    def ads(self) -> list[IAds] | None:  # TODO: モデルに
        return self.__meta_common.get('ads')

    @property
    def translator_available(self) -> bool:
        return self.__meta_common.get('translator_available', False)

    @property
    def email_required_for_signup(self) -> bool:
        return self.__meta_common.get('email_required_for_signup', False)

    @property
    def mascot_image_url(self) -> str | None:
        return self.__meta_common.get('mascot_image_url')

    # v12とv11の共通情報

    @property
    def emojis(self) -> list[CustomEmoji]:
        return (
            [
                CustomEmoji(i, client=self.__client)
                for i in self.__meta_common['emojis']
            ]
            if 'emojis' in self.__meta_common
            else []
        )


class LiteMeta(MetaCommon):
    def __init__(self, meta: ILiteMeta, *, client: ClientManager) -> None:
        super().__init__(meta, client=client)

        self.__lite_meta: ILiteMeta = meta

    @property
    def description(self) -> str | None:
        return self.__lite_meta['description']

    @property
    def disable_registration(self) -> bool:
        return self.__lite_meta['disable_registration']

    @property
    def feedback_url(self) -> str:
        return self.__lite_meta['feedback_url']

    @property
    def maintainer_email(self) -> str | None:
        return self.__lite_meta['maintainer_email']

    @property
    def maintainer_name(self) -> str | None:
        return self.__lite_meta['maintainer_name']

    @property
    def name(self) -> str | None:
        return self.__lite_meta['name']

    @property
    def repository_url(self) -> str:
        return self.__lite_meta['repository_url']

    @property
    def tos_url(self) -> str | None:
        return self.__lite_meta['tos_url']

    @property
    def uri(self) -> str:
        return self.__lite_meta['uri']

    @property
    def version(self) -> str:
        return self.__lite_meta['version']

    # v12のMeta

    @property
    def background_image_url(self) -> str | None:
        return self.__lite_meta.get('background_image_url')

    @property
    def default_dark_theme(self) -> str | None:
        return self.__lite_meta.get('default_dark_theme')

    @property
    def default_light_theme(self) -> str | None:
        return self.__lite_meta.get('default_light_theme')

    @property
    def logo_image_url(self) -> str | None:
        return self.__lite_meta.get('logo_image_url')

    @property
    def theme_color(self) -> str | None:
        return self.__lite_meta.get('theme_color')

    # v11のMeta

    @property
    def announcements(self) -> list[IAnnouncement] | None:  # TODO: 型確認
        return self.__lite_meta.get('announcements', None)

    @property
    def cpu(self) -> CPU | None:
        return (
            CPU(self.__lite_meta['cpu']) if 'cpu' in self.__lite_meta else None
        )

    @property
    def disable_local_timeline(self) -> bool:
        return self.__lite_meta.get('disable_local_timeline', False)

    @property
    def disable_global_timeline(self) -> bool:
        return self.__lite_meta.get('disable_global_timeline', False)

    @property
    def enable_emoji_reaction(self) -> bool:
        return self.__lite_meta.get('enable_emoji_reaction', False)

    @property
    def machine(self) -> str | None:
        return self.__lite_meta.get('machine')

    @property
    def node(self) -> str | None:
        return self.__lite_meta.get('node')

    @property
    def os(self) -> str | None:
        return self.__lite_meta.get('os')

    @property
    def proxy_account(self) -> str | None:
        return self.__lite_meta.get('proxy_account')

    @property
    def proxy_remote_files(self) -> bool:
        return self.__lite_meta.get('proxy_remote_files', False)

    @property
    def psql(self) -> str | None:
        return self.__lite_meta.get('psql')

    @property
    def redis(self) -> str | None:
        return self.__lite_meta.get('redis')

    @property
    def secure(self) -> bool:
        return self.__lite_meta.get('secure', False)

    @property
    def summaly_proxy(self) -> str | None:
        return self.__lite_meta.get('summaly_proxy')

    @property
    def tos_text_url(self) -> str | None:
        return self.__lite_meta.get('tos_text_url')

    @property
    def turnstile_secret_key(self) -> str | None:
        return self.__lite_meta.get('turnstile_secret_key')
