from typing import TypedDict


class IApp(TypedDict):
    id: str
    name: str
    callback_url: str | None
    permission: list[str]
    secret: str
    is_authorized: bool
