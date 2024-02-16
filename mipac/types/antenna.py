from typing import Literal, TypedDict

IAntennaReceiveSource = Literal["home", "all", "users", "list"]


class IAntenna(TypedDict):
    id: str
    created_at: str
    name: str
    keywords: list[str]
    exclude_keywords: list[str]
    src: IAntennaReceiveSource
    user_list_id: str | None
    users: list[str]
    case_sensitive: bool
    local_only: bool
    notify: bool
    with_replies: bool
    with_file: bool
    is_active: bool
    has_unread_note: bool
