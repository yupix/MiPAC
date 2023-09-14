from typing import Literal, TypedDict

IAntennaReceiveSource = Literal["home", "all", "users", "list"]


class IAntenna(TypedDict):
    case_sensitive: bool
    created_at: str
    exclude_keywords: list[str]
    has_unread_note: bool
    id: str
    is_actor: bool
    keywords: list[str]
    name: str
    notify: bool
    src: IAntennaReceiveSource
    user_list_id: str | None
    users: list[str]
    with_file: bool
    with_replies: bool
