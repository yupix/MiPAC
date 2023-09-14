from typing import Literal, TypedDict


class IAds(TypedDict):
    id: str
    ratio: int
    place: str
    url: str
    image_url: str


class IAd(TypedDict):
    id: str
    created_at: str
    starts_at: int
    expires_at: int
    url: str
    place: Literal["square" "horizontal" "horizontal-big"]
    priority: Literal["high" "middle" "low"]
    ratio: int
    image_url: str
    memo: str | None
