from typing import NotRequired, TypedDict


class IApp(TypedDict):
    id: str
    name: str
    callback_url: str | None
    permission: list[str]
    secret: NotRequired[str]
    is_authorized: NotRequired[bool]
