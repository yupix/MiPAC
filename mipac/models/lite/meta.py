from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.models.emoji import CustomEmoji
from mipac.types.ads import IAds

from mipac.types.meta import (
    ICPU,
    IAnnouncement,
    IFeatures,
    ILiteMeta,
    IPolicies,
)

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class CPU:
    def __init__(self, cpu: ICPU) -> None:
        self.__cpu: ICPU = cpu

    @property
    def cores(self) -> int:
        return self.__cpu['cores']

    @property
    def model(self) -> str:
        return self.__cpu['model']


class InstancePolicies:
    def __init__(self, policies: IPolicies) -> None:
        self.__policies: IPolicies = policies

    @property
    def gtl_available(self) -> bool:
        return self.__policies['gtl_available']

    @property
    def ltl_available(self) -> bool:
        return self.__policies['ltl_available']

    @property
    def can_public_note(self) -> bool:
        return self.__policies['can_public_note']

    @property
    def can_invite(self) -> bool:
        return self.__policies['can_invite']

    @property
    def can_manage_custom_emojis(self) -> bool:
        return self.__policies['can_manage_custom_emojis']

    @property
    def can_hide_ads(self) -> bool:
        return self.__policies['can_hide_ads']

    @property
    def drive_capacity_mb(self) -> int:
        return self.__policies['drive_capacity_mb']

    @property
    def pin_limit(self) -> int:
        return self.__policies['pin_limit']

    @property
    def antenna_limit(self) -> int:
        return self.__policies['antenna_limit']

    @property
    def word_mute_limit(self) -> int:
        return self.__policies['word_mute_limit']

    @property
    def webhook_limit(self) -> int:
        return self.__policies['webhook_limit']

    @property
    def clip_limit(self) -> int:
        return self.__policies['clip_limit']

    @property
    def note_each_clips_limit(self) -> int:
        return self.__policies['note_each_clips_limit']

    @property
    def user_list_limit(self) -> int:
        return self.__policies['user_list_limit']

    @property
    def user_each_user_lists_limit(self) -> int:
        return self.__policies['user_each_user_lists_limit']

    @property
    def rate_limit_factor(self) -> int:
        return self.__policies['rate_limit_factor']


class Features:
    def __init__(self, features: IFeatures, *, client: ClientActions) -> None:
        self.__features = features

    @property
    def registration(self) -> bool:
        return self.__features['registration']

    @property
    def elasticsearch(self) -> bool:
        return self.__features['elasticsearch']

    @property
    def hcaptcha(self) -> bool:
        return self.__features['hcaptcha']

    @property
    def recaptcha(self) -> bool:
        return self.__features['recaptcha']

    @property
    def object_storage(self) -> bool:
        return self.__features['object_storage']

    @property
    def twitter(self) -> bool:
        return self.__features['twitter']

    @property
    def github(self) -> bool:
        return self.__features['github']

    @property
    def discord(self) -> bool:
        return self.__features['discord']

    @property
    def service_worker(self) -> bool:
        return self.__features['service_worker']

    @property
    def miauth(self) -> bool:
        return self.__features['miauth']

    @property
    def email_required_for_signup(self) -> bool:
        return self.__features['email_required_for_signup']

    @property
    def global_time_line(self) -> bool:
        return self.__features['global_time_line']

    @property
    def local_time_line(self) -> bool:
        return self.__features['local_time_line']


class LiteMeta:
    def __init__(self, meta: ILiteMeta, *, client: ClientActions) -> None:
        self.__meta: ILiteMeta = meta
        self.__client: ClientActions = client

    @property
    def banner_url(self) -> str | None:
        return self.__meta['banner_url']

    @property
    def cache_remote_files(self) -> bool:
        return self.__meta['cache_remote_files']

    @property
    def description(self) -> str | None:
        return self.__meta['description']

    @property
    def disable_registration(self) -> bool:
        return self.__meta['disable_registration']

    @property
    def enable_discord_integration(self) -> bool:
        return self.__meta['enable_discord_integration']

    @property
    def enable_github_integration(self) -> bool:
        return self.__meta['enable_github_integration']

    @property
    def enable_service_worker(self) -> bool:
        return self.__meta['enable_service_worker']

    @property
    def enable_twitter_integration(self) -> bool:
        return self.__meta['enable_twitter_integration']

    @property
    def feedback_url(self) -> str:
        return self.__meta['feedback_url']

    @property
    def maintainer_email(self) -> str | None:
        return self.__meta['maintainer_email']

    @property
    def maintainer_name(self) -> str | None:
        return self.__meta['maintainer_name']

    @property
    def max_note_text_length(self) -> int:
        return self.__meta['max_note_text_length']

    @property
    def name(self) -> str | None:
        return self.__meta['name']

    @property
    def recaptcha_site_key(self) -> str:
        return self.__meta['recaptcha_site_key']

    @property
    def repository_url(self) -> str:
        return self.__meta['repository_url']

    @property
    def sw_publickey(self) -> str | None:
        return self.__meta['sw_publickey']

    @property
    def tos_url(self) -> str | None:
        return self.__meta['tos_url']

    @property
    def uri(self) -> str:
        return self.__meta['uri']

    @property
    def version(self) -> str:
        return self.__meta['version']

    # v12のMeta

    @property
    def ads(self) -> list[IAds] | None:  # TODO: モデルに
        return self.__meta.get('ads')

    @property
    def background_image_url(self) -> str | None:
        return self.__meta.get('background_image_url')

    @property
    def default_dark_theme(self) -> str | None:
        return self.__meta.get('default_dark_theme')

    @property
    def default_light_theme(self) -> str | None:
        return self.__meta.get('default_light_theme')

    @property
    def mascot_image_url(self) -> str | None:
        return self.__meta.get('mascot_image_url')

    @property
    def email_required_for_signup(self) -> bool:
        return self.__meta.get('email_required_for_signup', False)

    @property
    def logo_image_url(self) -> str | None:
        return self.__meta.get('logo_image_url')

    @property
    def translator_available(self) -> bool:

        return self.__meta.get('translator_available', False)

    @property
    def theme_color(self) -> str | None:
        return self.__meta.get('theme_color')

    # v11のMeta

    @property
    def announcements(self) -> list[IAnnouncement] | None:  # TODO: 型確認
        return self.__meta.get('announcements', None)

    @property
    def blocked_hosts(self) -> list[str]:
        return self.__meta.get('blocked_hosts', [])

    @property
    def cpu(self) -> CPU | None:
        return CPU(self.__meta['cpu']) if 'cpu' in self.__meta else None

    @property
    def disable_local_timeline(self) -> bool:
        return self.__meta.get('disable_local_timeline', False)

    @property
    def disable_global_timeline(self) -> bool:
        return self.__meta.get('disable_global_timeline', False)

    @property
    def discord_client_id(self) -> str | None:
        return self.__meta.get('discord_client_id')

    @property
    def discord_client_secret(self) -> str | None:
        return self.__meta.get('discord_client_secret')

    @property
    def drive_capacity_per_local_user_mb(self) -> int | None:
        return self.__meta.get('drive_capacity_per_local_user_mb')

    @property
    def drive_capacity_per_remote_user_mb(self) -> int | None:
        return self.__meta.get('drive_capacity_per_remote_user_mb')

    @property
    def email(self) -> str | None:
        return self.__meta.get('email')

    @property
    def enable_emoji_reaction(self) -> bool:
        return self.__meta.get('enable_emoji_reaction', False)

    @property
    def github_client_id(self) -> str | None:
        return self.__meta.get('github_client_id')

    @property
    def github_client_secret(self) -> str | None:
        return self.__meta.get('github_client_secret')

    @property
    def hidden_tags(self) -> list[str]:
        return self.__meta.get('hidden_tags', [])

    @property
    def machine(self) -> str | None:
        return self.__meta.get('machine')

    @property
    def node(self) -> str | None:
        return self.__meta.get('node')

    @property
    def object_storage_access_key(self) -> str | None:
        return self.__meta.get('object_storage_access_key')

    @property
    def object_storage_base_url(self) -> str | None:
        return self.__meta.get('object_storage_base_url')

    @property
    def object_storage_bucket(self) -> str | None:
        return self.__meta.get('object_storage_bucket')

    @property
    def object_storage_endpoint(self) -> str | None:
        return self.__meta.get('object_storage_endpoint')

    @property
    def object_storage_port(self) -> int | None:
        return self.__meta.get('object_storage_port')

    @property
    def object_storage_prefix(self) -> str | None:
        return self.__meta.get('object_storage_prefix')

    @property
    def object_storage_region(self) -> str | None:
        return self.__meta.get('object_storage_region')

    @property
    def object_storage_s3_force_path_style(self) -> bool:
        return self.__meta.get('object_storage_s3_force_path_style', False)

    @property
    def object_storage_secret_key(self) -> str | None:
        return self.__meta.get('object_storage_secret_key')

    @property
    def object_storage_set_public_read(self) -> bool:
        return self.__meta.get('object_storage_set_public_read', False)

    @property
    def object_storage_use_proxy(self) -> bool:
        return self.__meta.get('object_storage_use_proxy', False)

    @property
    def object_storage_use_ssl(self) -> bool:
        return self.__meta.get('object_storage_use_ssl', False)

    @property
    def os(self) -> str | None:
        return self.__meta.get('os')

    @property
    def pinned_users(self) -> list[str]:
        return self.__meta.get('pinned_users', [])

    @property
    def proxy_account(self) -> str | None:
        return self.__meta.get('proxy_account')

    @property
    def proxy_remote_files(self) -> bool:
        return self.__meta.get('proxy_remote_files', False)

    @property
    def psql(self) -> str | None:
        return self.__meta.get('psql')

    @property
    def recaptcha_secret_key(self) -> str | None:
        return self.__meta.get('recaptcha_secret_key')

    @property
    def redis(self) -> str | None:
        return self.__meta.get('redis')

    @property
    def secure(self) -> bool:
        return self.__meta.get('secure', False)

    @property
    def smtp_host(self) -> str | None:
        return self.__meta.get('smtp_host')

    @property
    def smtp_pass(self) -> str | None:
        return self.__meta.get('smtp_pass')

    @property
    def smtp_port(self) -> int | None:
        return self.__meta.get('smtp_port')

    @property
    def smtp_secure(self) -> bool:
        return self.__meta.get('smtp_secure', False)

    @property
    def smtp_user(self) -> str | None:
        return self.__meta.get('smtp_user')

    @property
    def summaly_proxy(self) -> str | None:
        return self.__meta.get('summaly_proxy')

    @property
    def sw_private_key(self) -> str | None:
        return self.__meta.get('sw_private_key')

    @property
    def tos_text_url(self) -> str | None:
        return self.__meta.get('tos_text_url')

    @property
    def turnstile_secret_key(self) -> str | None:
        return self.__meta.get('turnstile_secret_key')

    @property
    def twitter_consumer_key(self) -> str | None:
        return self.__meta.get('twitter_consumer_key')

    @property
    def twitter_consumer_secret(self) -> str | None:
        return self.__meta.get('twitter_consumer_secret')

    @property
    def use_object_storage(self) -> bool:
        return self.__meta.get('use_object_storage', False)

    @property
    def use_star_for_reaction_fallback(self) -> bool:
        return self.__meta.get('use_star_for_reaction_fallback', False)

    @property
    def emojis(self) -> list[CustomEmoji]:
        return (
            [
                CustomEmoji(i, client=self.__client)
                for i in self.__meta['emojis']
            ]
            if 'emojis' in self.__meta
            else []
        )
