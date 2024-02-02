from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict, TypeGuard

if TYPE_CHECKING:
    from mipac.types.user import IMeDetailedSchema, IUserDetailed


class IRoleUser(TypedDict):
    id: str
    user: IUserDetailed
    expires_at: str | None


class IMeRole(TypedDict):
    id: str
    user: IMeDetailedSchema
    expires_at: str | None


class IRolePolicieValue(TypedDict):
    value: int
    use_default: bool
    priority: NotRequired[int]


class IRolePolicies(TypedDict):
    antenna_limit: IRolePolicieValue
    gtl_available: IRolePolicieValue
    ltl_available: IRolePolicieValue
    can_public_note: IRolePolicieValue
    drive_capacity_mb: IRolePolicieValue
    can_invite: IRolePolicieValue
    can_manage_custom_emojis: IRolePolicieValue
    can_hide_ads: IRolePolicieValue
    pin_limit: IRolePolicieValue
    word_mute_limit: IRolePolicieValue
    webhook_limit: IRolePolicieValue
    clip_limit: IRolePolicieValue
    note_each_clips_limit: IRolePolicieValue
    user_list_limit: IRolePolicieValue
    user_each_user_lists_limit: IRolePolicieValue
    rate_limit_factor: IRolePolicieValue


class IPartialRole(TypedDict):
    id: str
    name: str
    color: str | None
    icon_url: str | None
    description: str  # 空でもNoneではない
    is_moderator: bool
    is_administrator: bool
    display_order: int


class IRole(IPartialRole):
    created_at: str
    updated_at: str
    target: Literal["manual", "conditional"]
    cond_formula: dict
    is_public: bool
    is_explorable: bool
    as_badge: bool
    can_edit_members_by_moderator: bool
    policies: IRolePolicies
    users_count: int


def is_me_role(data: IMeRole | IRoleUser, me_id: str) -> TypeGuard[IMeRole]:
    return data["user"]["id"] == me_id and data["user"].get("avatar_id") is not None
