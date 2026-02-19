from typing import Literal, TypedDict

IAdPlaces = Literal["square", "horizontal", "horizontal-big"]
IAdPriority = Literal["high", "middle", "low"]


class IAd(TypedDict):
    id: str
    expires_at: str
    starts_at: str
    place: IAdPlaces
    priority: IAdPriority
    ratio: int
    url: str
    image_url: str
    memo: str
    day_of_week: int
    is_sensitive: bool
