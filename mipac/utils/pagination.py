from __future__ import annotations

from typing import Any, Literal

from mipac.http import HTTPClient, Route


class Pagination[T]:
    def __init__(
        self,
        http_client: HTTPClient,
        route: Route,
        json: dict[str, Any],
        auth: bool = True,
        remove_none: bool = True,
        lower: bool = True,
        pagination_type: Literal["until", "count"] = "until",
        limit: int = 100,
    ) -> None:
        self.http_client: HTTPClient = http_client
        self.route: Route = route
        self.json: dict[str, Any] = json
        self.auth: bool = auth
        self.remove_none: bool = remove_none
        self.lower: bool = lower
        self.pagination_type: Literal["until", "count"] = pagination_type
        self.limit: int = limit
        self.count = 0
        self.next_id: str = ""
        self.latest_res_count: int | None = None

    async def next(self) -> list[T]:
        if self.pagination_type == "count":
            self.json["offset"] = self.json.get("limit", self.limit) * self.count
            self.count += 1
        res: list[T] = await self.http_client.request(
            self.route,
            auth=self.auth,
            remove_none=self.remove_none,
            lower=self.lower,
            json=self.json,
        )
        if self.pagination_type == "until":
            if len(res) > 0:
                self.next_id = res[-1]["id"]  # type: ignore
            self.json["untilId"] = self.next_id
        self.latest_res_count = len(res)
        return res

    @property
    def is_final(self) -> bool:
        if self.latest_res_count is None:
            return False

        match self.pagination_type:
            case "count":
                return self.latest_res_count == 0
            case "until":
                return self.latest_res_count == 0
            case _:
                raise ValueError("Invalid pagination type")
