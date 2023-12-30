from __future__ import annotations

from typing import TypedDict


class IFederationInstanceStat(TypedDict):
    top_sub_instances: list[IFederationInstance]
    other_followers_count: int
    top_pub_instances: list[IFederationInstance]
    other_following_count: int


class IFederationInstanceRequired(TypedDict):
    id: str
    host: str
    users_count: int
    notes_count: int
    following_count: int
    followers_count: int
    is_not_responding: bool
    is_suspended: bool
    is_blocked: bool
    software_name: str
    software_version: str
    open_registrations: bool
    name: str
    description: str
    maintainer_name: str
    maintainer_email: str
    icon_url: str
    favicon_url: str
    theme_color: str
    info_updated_at: str


class IFederationInstance(IFederationInstanceRequired, total=False):
    caught_at: str
    first_retrieved_at: str
    latest_request_sent_at: str
    last_communicated_at: str


class IInstanceLite(TypedDict):
    name: str | None
    software_name: str | None
    software_version: str | None
    icon_url: str | None
    favicon_url: str | None
    theme_color: str | None
