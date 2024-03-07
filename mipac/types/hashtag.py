from typing import TypedDict


class IHashtag(TypedDict):
    tag: str
    mentioned_users_count: int
    mentioned_local_users_count: int
    mentioned_remote_users_count: int
    attached_users_count: int
    attached_local_users_count: int
    attached_remote_users_count: int


class ITrendHashtag(TypedDict):
    tag: str
    chart: list[int]
    users_count: int
