from __future__ import annotations

from typing import TYPE_CHECKING
from mipac.models.lite.meta import LiteMeta, MetaCommon
from mipac.types.meta import (
    IAdminMeta,
    IFeatures,
    IMeta,
    IPolicies,
)

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class Policies:
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
    def __init__(self, features: IFeatures) -> None:
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
        return self.__features.get('miauth', False)

    @property
    def email_required_for_signup(self) -> bool:
        return self.__features.get('email_required_for_signup', False)

    @property
    def global_time_line(self) -> bool:
        return self.__features.get('global_time_line', False)

    @property
    def local_time_line(self) -> bool:
        return self.__features.get('local_time_line', False)


class Meta(LiteMeta):
    def __init__(self, meta: IMeta, *, client: ClientManager) -> None:
        super().__init__(meta, client=client)
        self.__meta = meta

    # shared

    @property
    def features(self) -> Features:
        return Features(self.__meta['features'])

    # v12

    @property
    def pinned_clip_id(self) -> str | None:
        return self.__meta.get('pinned_clip_id')

    @property
    def pinned_pages(self) -> list[str]:
        return self.__meta.get('pinned_pages', [])

    @property
    def policies(self) -> Policies | None:
        return (
            Policies(self.__meta['policies'])
            if 'policies' in self.__meta
            else None
        )

    @property
    def require_setup(self) -> bool:
        return self.__meta.get('require_setup', False)


class AdminMeta(MetaCommon):
    def __init__(
        self, admin_meta: IAdminMeta, *, client: ClientManager
    ) -> None:
        super().__init__(admin_meta, client=client)
        self.__admin_meta = admin_meta

    # 全てのバージョン共通に存在する

    @property
    def drive_capacity_per_local_user_mb(self) -> int | None:
        return self.__admin_meta.get('drive_capacity_per_local_user_mb')

    @property
    def drive_capacity_per_remote_user_mb(self) -> int | None:
        return self.__admin_meta.get('drive_capacity_per_remote_user_mb')

    @property
    def hidden_tags(self) -> list[str]:
        return self.__admin_meta.get('hidden_tags', [])

    @property
    def blocked_hosts(self) -> list[str]:
        return self.__admin_meta.get('blocked_hosts', [])

    @property
    def recaptcha_secret_key(self) -> str | None:
        return self.__admin_meta.get('recaptcha_secret_key')

    @property
    def twitter_consumer_key(self) -> str | None:
        return self.__admin_meta.get('twitter_consumer_key')

    @property
    def twitter_consumer_secret(self) -> str | None:
        return self.__admin_meta.get('twitter_consumer_secret')

    @property
    def github_client_id(self) -> str | None:
        return self.__admin_meta.get('github_client_id')

    @property
    def github_client_secret(self) -> str | None:
        return self.__admin_meta.get('github_client_secret')

    @property
    def discord_client_id(self) -> str | None:
        return self.__admin_meta.get('discord_client_id')

    @property
    def discord_client_secret(self) -> str | None:
        return self.__admin_meta.get('discord_client_secret')

    @property
    def email(self) -> str | None:
        return self.__admin_meta.get('email')

    @property
    def smtp_secure(self) -> bool:
        return self.__admin_meta.get('smtp_secure', False)

    @property
    def smtp_host(self) -> str | None:
        return self.__admin_meta.get('smtp_host')

    @property
    def smtp_port(self) -> int | None:
        return self.__admin_meta.get('smtp_port')

    @property
    def smtp_user(self) -> str | None:
        return self.__admin_meta.get('smtp_user')

    @property
    def smtp_pass(self) -> str | None:
        return self.__admin_meta.get('smtp_pass')

    @property
    def sw_private_key(self) -> str | None:
        return self.__admin_meta.get('sw_private_key')

    @property
    def use_object_storage(self) -> bool:
        return self.__admin_meta.get('use_object_storage', False)

    @property
    def object_storage_base_url(self) -> str | None:
        return self.__admin_meta.get('object_storage_base_url')

    @property
    def object_storage_bucket(self) -> str | None:
        return self.__admin_meta.get('object_storage_bucket')

    @property
    def object_storage_prefix(self) -> str | None:
        return self.__admin_meta.get('object_storage_prefix')

    @property
    def object_storage_endpoint(self) -> str | None:
        return self.__admin_meta.get('object_storage_endpoint')

    @property
    def object_storage_region(self) -> str | None:
        return self.__admin_meta.get('object_storage_region')

    @property
    def object_storage_port(self) -> int | None:
        return self.__admin_meta.get('object_storage_port')

    @property
    def object_storage_access_key(self) -> str | None:
        return self.__admin_meta.get('object_storage_access_key')

    @property
    def object_storage_secret_key(self) -> str | None:
        return self.__admin_meta.get('object_storage_secret_key')

    @property
    def object_storage_use_ssl(self) -> bool:
        return self.__admin_meta.get('object_storage_use_ssl', False)

    @property
    def object_storage_use_proxy(self) -> bool:
        return self.__admin_meta.get('object_storage_use_proxy', False)

    @property
    def object_storage_set_public_read(self) -> bool:
        return self.__admin_meta.get('object_storage_set_public_read', False)

    @property
    def pinned_users(self) -> list[str]:
        return self.__admin_meta.get('pinned_users', [])

    """
    v12 only
    """

    @property
    def hcaptcha_secret_key(self) -> str | None:
        return self.__admin_meta.get('hcaptcha_secret_key')

    @property
    def sensitive_media_detection(self) -> str | None:
        return self.__admin_meta.get('sensitive_media_detection')

    @property
    def sensitive_media_detection_sensitivity(self) -> str | None:
        return self.__admin_meta.get('sensitive_media_detection_sensitivity')

    @property
    def set_sensitive_flag_automatically(self) -> bool:
        return self.__admin_meta.get('set_sensitive_flag_automatically', False)

    @property
    def enable_sensitive_media_detection_for_videos(self) -> bool:
        return self.__admin_meta.get(
            'enable_sensitive_media_detection_for_videos', False
        )

    @property
    def proxy_account_id(self) -> str | None:
        return self.__admin_meta.get('proxy_account_id')

    @property
    def summary_proxy(self) -> str | None:
        return self.__admin_meta.get('summary_proxy')

    @property
    def enable_ip_logging(self) -> bool:
        return self.__admin_meta.get('enable_ip_logging', False)

    @property
    def enable_active_email_validation(self) -> bool:
        return self.__admin_meta.get('enable_active_email_validation', False)
