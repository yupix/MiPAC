from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from mipac.http import HTTPClient, Route
from mipac.utils.format import str_to_datetime


def _parse_date_to_timestamp_ms(value: str | int) -> int:
    """日付をUnixタイムスタンプ（ミリ秒）に変換します"""
    if isinstance(value, int):
        return value
    try:
        dt = str_to_datetime(value)
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp() * 1000)


class Pagination[T]:
    """ページネーションを行うためのクラスです"""

    def __init__(
        self,
        http_client: HTTPClient,
        route: Route,
        json: dict[str, Any],
        auth: bool = True,
        remove_none: bool = True,
        lower: bool = True,
        pagination_type: Literal["until", "until_date", "since_date", "count"] = "until",
        limit: int = 100,
        date_key: str = "created_at",
    ) -> None:
        self.http_client: HTTPClient = http_client
        self.route: Route = route
        self.json: dict[str, Any] = json
        self.auth: bool = auth
        self.remove_none: bool = remove_none
        self.lower: bool = lower
        self.pagination_type: Literal["until", "until_date", "since_date", "count"] = pagination_type
        self.limit: int = limit
        self.date_key: str = date_key
        self.count = 0
        self.next_id: str = ""
        self.next_date: int = 0
        self.latest_res_count: int | None = None

    async def next(self) -> list[T]:
        """次のページを取得します

        Returns
        -------
        list
            取得したページの戻り値
        """
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
        elif self.pagination_type == "until_date":
            if len(res) > 0 and isinstance(last_item := res[-1], dict):
                date_value = last_item.get(self.date_key) or last_item.get("createdAt")
                if date_value is not None:
                    self.next_date = _parse_date_to_timestamp_ms(date_value)
                    self.json["untilDate"] = self.next_date
        elif self.pagination_type == "since_date":
            if len(res) > 0 and isinstance(first_item := res[0], dict):
                date_value = first_item.get(self.date_key) or first_item.get("createdAt")
                if date_value is not None:
                    self.next_date = _parse_date_to_timestamp_ms(date_value)
                    self.json["sinceDate"] = self.next_date
        self.latest_res_count = len(res)
        return res

    @property
    def is_final(self) -> bool:
        """現在のページネーションが最後の戻り値かを返します

        Returns
        -------
        bool
            最後の戻り値かどうか
        """
        if self.latest_res_count is None:
            return False

        match self.pagination_type:
            case "count":
                return self.latest_res_count == 0
            case "until" | "until_date" | "since_date":
                return self.latest_res_count == 0
            case _:
                raise ValueError("Invalid pagination type")
