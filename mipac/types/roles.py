from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict


if TYPE_CHECKING:
    from mipac.types.user import IUserDetailedNotMeSchema
    from mipac.types.user import IMeDetailedSchema


class IRoleUser(TypedDict):
    id: str
    created_at: str
    user: IUserDetailedNotMeSchema | IMeDetailedSchema
    expires_at: str | None


class IRolePolicies(TypedDict):
    gtl_available: bool
    ltl_available: bool
    can_public_note: bool
    can_invite: bool
    invite_limit: int
    invite_limit_cycle: int
    invite_expiration_time: int
    can_manage_custom_emojis: bool
    can_manage_avatar_decorations: bool
    can_search_notes: bool
    can_use_translator: bool
    can_hide_ads: bool
    drive_capacity_mb: int
    always_mark_nfsw: bool
    pin_limit: int
    antenna_limit: int
    word_mute_limit: int
    webhook_limit: int
    clip_limit: int
    note_each_clips_limit: int
    user_list_limit: int
    user_each_user_lists_limit: int
    rate_limit_factor: int
    avatar_decoration_limit: int


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
