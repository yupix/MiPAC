from typing import TypedDict


class IAvatarDecoration(TypedDict):
    id: str
    created_at: str
    updated_at: str | None
    name: str
    description: str
    category: str | None
    url: str
    role_ids_that_can_be_used_this_decoration: list[str]
