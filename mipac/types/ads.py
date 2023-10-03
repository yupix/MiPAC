from typing import Literal, TypedDict


IAdPlaces = Literal["square" "horizontal" "horizontal-big"]

class IPartialAd(TypedDict):
    id: str
    url: str
    place: IAdPlaces
    ratio: int
    image_url: str
    day_of_week: int


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
