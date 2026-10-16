import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from mipac.errors.base import APIError
from mipac.errors.errors import NoSuchNoteError
from mipac.http import HTTPClient, Route

received: list[dict] = []


async def show(request: web.Request) -> web.Response:
    received.append(await request.json())
    return web.json_response({"id": "1", "createdAt": "2024-01-01T00:00:00.000Z"})


async def no_content(request: web.Request) -> web.Response:
    return web.Response(status=204)


async def api_error(request: web.Request) -> web.Response:
    return web.json_response(
        {"error": {"code": "NO_SUCH_NOTE", "id": "x", "message": "No such note."}}, status=400
    )


async def text_error(request: web.Request) -> web.Response:
    return web.Response(status=500, text="boom")


@pytest.fixture
async def client():
    app = web.Application()
    app.router.add_post("/api/notes/show", show)
    app.router.add_post("/api/empty", no_content)
    app.router.add_post("/api/error", api_error)
    app.router.add_post("/api/text-error", text_error)
    server = TestServer(app)
    await server.start_server()
    http = HTTPClient(f"http://{server.host}:{server.port}", token="secret")
    received.clear()
    yield http
    await http.close_session()
    await server.close()


async def test_request_injects_token_drops_none_and_lowercases_response(client: HTTPClient):
    data = await client.request(Route("POST", "/api/notes/show"), json={"noteId": "1", "x": None})
    assert received == [{"noteId": "1", "i": "secret"}]
    assert data == {"id": "1", "created_at": "2024-01-01T00:00:00.000Z"}


async def test_request_returns_true_on_204(client: HTTPClient):
    assert await client.request(Route("POST", "/api/empty")) is True


async def test_request_raises_mapped_error_for_api_error(client: HTTPClient):
    with pytest.raises(NoSuchNoteError) as exc:
        await client.request(Route("POST", "/api/error"))
    assert exc.value.status == 400
    assert exc.value.code == "NO_SUCH_NOTE"


async def test_request_raises_api_error_for_non_json_error(client: HTTPClient):
    with pytest.raises(APIError) as exc:
        await client.request(Route("POST", "/api/text-error"))
    assert exc.value.status == 500
