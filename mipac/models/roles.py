from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.models.lite.role import PartialRole
from mipac.types.roles import IRole, IRolePolicies

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class RolePolicies:
    def __init__(self, role_policies_data: IRolePolicies) -> None:
        self.__role_policies_data = role_policies_data

    @property
    def gtl_available(self) -> bool:
        return self.__role_policies_data["gtl_available"]

    @property
    def ltl_available(self) -> bool:
        return self.__role_policies_data["ltl_available"]

    @property
    def can_public_note(self) -> bool:
        return self.__role_policies_data["can_public_note"]

    @property
    def mention_limit(self) -> int:
        return self.__role_policies_data["mention_limit"]

    @property
    def can_invite(self) -> bool:
        return self.__role_policies_data["can_invite"]

    @property
    def invite_limit(self) -> int:
        return self.__role_policies_data["invite_limit"]

    @property
    def invite_limit_cycle(self) -> int:
        return self.__role_policies_data["invite_limit_cycle"]

    @property
    def invite_expiration_time(self) -> int:
        return self.__role_policies_data["invite_expiration_time"]

    @property
    def can_manage_custom_emojis(self) -> bool:
        return self.__role_policies_data["can_manage_custom_emojis"]

    @property
    def can_manage_avatar_decorations(self) -> bool:
        return self.__role_policies_data["can_manage_avatar_decorations"]

    @property
    def can_search_notes(self) -> bool:
        return self.__role_policies_data["can_search_notes"]

    @property
    def can_use_translator(self) -> bool:
        return self.__role_policies_data["can_use_translator"]

    @property
    def can_hide_ads(self) -> bool:
        return self.__role_policies_data["can_hide_ads"]

    @property
    def drive_capacity_mb(self) -> int:
        return self.__role_policies_data["drive_capacity_mb"]

    @property
    def always_mark_nfsw(self) -> bool:
        return self.__role_policies_data["always_mark_nfsw"]

    @property
    def can_update_bio_media(self) -> bool:
        return self.__role_policies_data["can_update_bio_media"]

    @property
    def pin_limit(self) -> int:
        return self.__role_policies_data["pin_limit"]

    @property
    def antenna_limit(self) -> int:
        return self.__role_policies_data["antenna_limit"]

    @property
    def word_mute_limit(self) -> int:
        return self.__role_policies_data["word_mute_limit"]

    @property
    def webhook_limit(self) -> int:
        return self.__role_policies_data["webhook_limit"]

    @property
    def clip_limit(self) -> int:
        return self.__role_policies_data["clip_limit"]

    @property
    def note_each_clips_limit(self) -> int:
        return self.__role_policies_data["note_each_clips_limit"]

    @property
    def user_list_limit(self) -> int:
        return self.__role_policies_data["user_list_limit"]

    @property
    def user_each_user_lists_limit(self) -> int:
        return self.__role_policies_data["user_each_user_lists_limit"]

    @property
    def rate_limit_factor(self) -> int:
        return self.__role_policies_data["rate_limit_factor"]

    @property
    def avatar_decoration_limit(self) -> int:
        return self.__role_policies_data["avatar_decoration_limit"]

    @property
    def can_import_antennas(self) -> bool:
        return self.__role_policies_data["can_import_antennas"]

    @property
    def can_import_blocking(self) -> bool:
        return self.__role_policies_data["can_import_blocking"]

    @property
    def can_import_following(self) -> bool:
        return self.__role_policies_data["can_import_following"]

    @property
    def can_import_muting(self) -> bool:
        return self.__role_policies_data["can_import_muting"]

    @property
    def can_import_user_lists(self) -> bool:
        return self.__role_policies_data["can_import_user_lists"]

    @property
    def can_create_channel(self) -> bool:
        return self.__role_policies_data["can_create_channel"]

    def _get(self, key: str) -> Any | None:
        return self.__role_policies_data.get(key)


class Role(PartialRole[IRole]):
    def __init__(self, role_data: IRole, *, client: ClientManager) -> None:
        super().__init__(role_data, client=client)

    @property
    def created_at(self) -> str:
        return self._raw_role["created_at"]

    @property
    def updated_at(self) -> str:
        return self._raw_role["updated_at"]

    @property
    def target(self) -> str:
        return self._raw_role["target"]

    @property
    def cond_formula(self) -> dict:
        return self._raw_role["cond_formula"]

    @property
    def is_public(self) -> bool:
        return self._raw_role["is_public"]

    @property
    def is_explorable(self) -> bool:
        return self._raw_role["is_explorable"]

    @property
    def as_badge(self) -> bool:
        return self._raw_role["as_badge"]

    @property
    def can_edit_members_by_moderator(self) -> bool:
        return self._raw_role["can_edit_members_by_moderator"]

    @property
    def policies(self) -> RolePolicies:
        return RolePolicies(self._raw_role["policies"])

    @property
    def users_count(self) -> int:
        return self._raw_role["users_count"]

    def _get(self, key: str) -> Any | None:
        return self._raw_role.get(key)
