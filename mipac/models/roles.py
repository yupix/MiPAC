from mipac.types.roles import IRole, IRolePolicies, IRolePolicieValue


class RolePolicyValue:
    def __init__(self, policiy_value_data: IRolePolicieValue) -> None:
        self.__policy_value_data = policiy_value_data

    @property
    def value(self) -> int:
        return self.__policy_value_data.get('value')

    @property
    def use_default(self) -> bool:
        return self.__policy_value_data.get('use_default')

    @property
    def priority(self) -> int | None:
        return self.__policy_value_data.get('priority')


class RolePolicies:
    def __init__(self, role_policies_data: IRolePolicies) -> None:
        self.__role_policies_data = role_policies_data

    @property
    def antenna_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('antenna_limit'))

    @property
    def gtl_available(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('gtl_available'))

    @property
    def ltl_available(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('ltl_available'))

    @property
    def can_public_note(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('can_public_note'))

    @property
    def drive_capacity_mb(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('drive_capacity_mb'))

    @property
    def can_invite(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('can_invite'))

    @property
    def can_manage_custom_emojis(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('can_manage_custom_emojis'))

    @property
    def can_hide_ads(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('can_hide_ads'))

    @property
    def pin_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('pin_limit'))

    @property
    def word_mute_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('word_mute_limit'))

    @property
    def webhook_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('webhook_limit'))

    @property
    def clip_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('clip_limit'))

    @property
    def note_each_clips_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('note_each_clips_limit'))

    @property
    def user_list_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('user_list_limit'))

    @property
    def user_each_user_lists_limit(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('user_each_user_lists_limit'))

    @property
    def rate_limit_factor(self) -> RolePolicyValue:
        return RolePolicyValue(self.__role_policies_data.get('rate_limit_factor'))


class Role:
    def __init__(self, role_data: IRole) -> None:
        self.__role_data: IRole = role_data

    @property
    def id(self) -> str:
        return self.__role_data.get('id')

    @property
    def created_at(self) -> str:
        return self.__role_data.get('created_at')

    @property
    def updated_at(self) -> str:
        return self.__role_data.get('updated_at')

    @property
    def name(self) -> str:
        return self.__role_data.get('name')

    @property
    def description(self) -> str:
        return self.__role_data.get('description')

    @property
    def color(self) -> str | None:
        return self.__role_data.get('color')

    @property
    def icon_url(self) -> str | None:
        return self.__role_data.get('icon_url')

    @property
    def target(self) -> str:
        return self.__role_data.get('target')

    @property
    def cond_formula(self) -> dict:
        return self.__role_data.get('cond_formula')

    @property
    def is_public(self) -> bool:
        return self.__role_data.get('is_public')

    @property
    def is_administrator(self) -> bool:
        return self.__role_data.get('is_administrator')

    @property
    def is_moderator(self) -> bool:
        return self.__role_data.get('is_moderator')

    @property
    def as_badge(self) -> bool:
        return self.__role_data.get('as_badge')

    @property
    def can_edit_members_by_moderator(self) -> bool:
        return self.__role_data.get('can_edit_members_by_moderator')

    @property
    def policies(self) -> RolePolicies:
        return RolePolicies(self.__role_data.get('policies'))

    @property
    def users_count(self) -> int:
        return self.__role_data.get('users_count')
