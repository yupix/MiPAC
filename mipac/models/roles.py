from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.abstract.model import AbstractModel
from mipac.models.lite.role import PartialRole
from mipac.models.user import MeDetailed, UserDetailed
from mipac.types.roles import IMeRole, IRole, IRolePolicies, IRolePolicieValue, IRoleUser
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.user import UserManager


class RoleUser(AbstractModel):
    def __init__(self, role_user: IRoleUser, *, client: ClientManager) -> None:
        self.__role_user = role_user
        self.__client = client

    @property
    def id(self) -> str:
        return self.__role_user["id"]

    @property
    def user(self) -> UserDetailed:
        return UserDetailed(self.__role_user["user"], client=self.__client)

    @property
    def expires_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__role_user["expires_at"])
            if self.__role_user["expires_at"]
            else None
        )

    @property
    def action(self) -> UserManager:
        return self.__client._create_user_instance(self.user)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, RoleUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class MeRole(AbstractModel):
    def __init__(self, data: IMeRole, *, client: ClientManager) -> None:
        self.__role_user = data
        self.__client = client

    @property
    def id(self) -> str:
        return self.__role_user["id"]

    @property
    def user(self) -> MeDetailed:
        return MeDetailed(self.__role_user["user"], client=self.__client)

    @property
    def expires_at(self) -> datetime | None:
        return (
            str_to_datetime(self.__role_user["expires_at"])
            if self.__role_user["expires_at"]
            else None
        )

    @property
    def action(self) -> UserManager:
        return self.__client._create_user_instance(self.user)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, RoleUser) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class RolePolicyValue(AbstractModel):
    def __init__(self, policiy_value_data: IRolePolicieValue) -> None:
        self.__policy_value_data = policiy_value_data

    @property
    def value(self) -> int:
        return self.__policy_value_data.get("value")

    @property
    def use_default(self) -> bool:
        return self.__policy_value_data.get("use_default")

    @property
    def priority(self) -> int | None:
        return self.__policy_value_data.get("priority")


class RolePolicies(AbstractModel):
    def __init__(self, role_policies_data: IRolePolicies) -> None:
        self.__role_policies_data = role_policies_data

    @property
    def antenna_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("antenna_limit"))

    @property
    def gtl_available(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("gtl_available"))

    @property
    def ltl_available(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("ltl_available"))

    @property
    def can_public_note(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("can_public_note"))

    @property
    def drive_capacity_mb(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("drive_capacity_mb"))

    @property
    def can_invite(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("can_invite"))

    @property
    def can_manage_custom_emojis(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("can_manage_custom_emojis"))

    @property
    def can_hide_ads(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("can_hide_ads"))

    @property
    def pin_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("pin_limit"))

    @property
    def word_mute_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("word_mute_limit"))

    @property
    def webhook_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("webhook_limit"))

    @property
    def clip_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("clip_limit"))

    @property
    def note_each_clips_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("note_each_clips_limit"))

    @property
    def user_list_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("user_list_limit"))

    @property
    def user_each_user_lists_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("user_each_user_lists_limit"))

    @property
    def rate_limit_factor(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get("rate_limit_factor"))


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
