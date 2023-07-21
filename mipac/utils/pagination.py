from typing import Any, Generic, Literal, TypeVar

from mipac.http import HTTPClient, Route

T = TypeVar('T')


class Pagination(Generic[T]):
    def __init__(
        self,
        http_client: HTTPClient,
        route: Route,
        json: dict[str, Any],
        auth: bool = True,
        remove_none: bool = True,
        lower: bool = True,
        pagination_type: Literal['until', 'count'] = 'until',
        can_use_limit: bool = True,
        limit: int = 100,
        max_limit: int = 100,
    ) -> None:
        self.http_client: HTTPClient = http_client
        self.route: Route = route
        self.json: dict[str, Any] = json
        self.auth: bool = auth
        self.remove_none: bool = remove_none
        self.lower: bool = lower
        self.pagination_type: Literal['until', 'count'] = pagination_type
        self.can_use_limit: bool = can_use_limit
        self.limit: int = limit
        self.max_limit: int = max_limit
        self.count = 0
        self.next_id: str = ''
        self.previous_id: str = ''
        self.latest_res_count: int = 0

    async def next(self) -> list[T]:
        if self.pagination_type == 'count':
            self.json['offset'] = self.json.get('limit', self.limit) * self.count
            self.count += 1
        res: list[T] = await self.http_client.request(
            self.route,
            auth=self.auth,
            remove_none=self.remove_none,
            lower=self.lower,
            json=self.json,
        )
        if self.pagination_type == 'until':
            self.previous_id = self.json.get('untilId', '')  # 前のIDを保存しておく
            if len(res) > 0:
                self.next_id = res[-1]['id']  # type: ignore
            self.json['untilId'] = self.next_id
        self.latest_res_count = len(res)
        return res

    @property
    def is_final(self) -> bool:
        if (
            self.pagination_type == 'count'
            and self.latest_res_count == 0
            or self.latest_res_count < self.max_limit
        ):
            return True
        if self.pagination_type == 'until' and self.latest_res_count == 0:
            return True
        return False
