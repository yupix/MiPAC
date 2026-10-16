from mipac.http import Route
from mipac.utils.pagination import Pagination, _infer_pagination_type


class FakeHTTPClient:
    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    async def request(self, route, **kwargs):
        self.calls.append(dict(kwargs["json"]))
        return self.pages.pop(0)


def test_infer_pagination_type_priority():
    assert (
        _infer_pagination_type({"untilDate": 1, "untilId": "x", "sinceDate": 1, "sinceId": "y"})
        == "until_date"
    )
    assert _infer_pagination_type({"untilId": "x", "sinceDate": 1, "sinceId": "y"}) == "until"
    assert _infer_pagination_type({"sinceDate": 1, "sinceId": "y"}) == "since_date"
    assert _infer_pagination_type({"sinceId": "y"}) == "since"
    assert _infer_pagination_type({"untilId": None}) == "until"


async def test_until_pagination_uses_last_id_and_detects_final_page():
    http = FakeHTTPClient([[{"id": "3"}, {"id": "2"}], []])
    pagination = Pagination(http, Route("POST", "/api/notes"), json={"untilId": None})
    assert pagination.is_final is False
    assert await pagination.next() == [{"id": "3"}, {"id": "2"}]
    assert pagination.json["untilId"] == "2"
    assert pagination.is_final is False
    assert await pagination.next() == []
    assert pagination.is_final is True


async def test_since_pagination_uses_first_id():
    http = FakeHTTPClient([[{"id": "3"}, {"id": "2"}]])
    pagination = Pagination(http, Route("POST", "/api/notes"), json={"sinceId": "1"})
    await pagination.next()
    assert pagination.json["sinceId"] == "3"


async def test_count_pagination_advances_offset_by_limit():
    http = FakeHTTPClient([[{"id": "1"}], [{"id": "2"}], []])
    pagination = Pagination(
        http, Route("POST", "/api/notes"), json={"limit": 10}, pagination_type="count"
    )
    await pagination.next()
    await pagination.next()
    await pagination.next()
    assert [c["offset"] for c in http.calls] == [0, 10, 20]
    assert pagination.is_final is True


async def test_until_date_pagination_uses_last_item_date():
    http = FakeHTTPClient([[{"id": "1", "created_at": 1700000000000}]])
    pagination = Pagination(http, Route("POST", "/api/notes"), json={"untilDate": 1800000000000})
    await pagination.next()
    assert pagination.json["untilDate"] == 1700000000000
