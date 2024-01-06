from typing import Literal, TypedDict

IAdPlaces = Literal["square" "horizontal" "horizontal-big"]
IAdPriority = Literal["high" "middle" "low"]


class IPartialAd(TypedDict):
    id: str
    url: str
    place: IAdPlaces
    ratio: int
    image_url: str
    day_of_week: int


class IAd(IPartialAd):
    expires_at: str
    starts_at: str
    priority: IAdPriority
    memo: str | None
