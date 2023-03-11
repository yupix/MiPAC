from typing import Any, Literal, TypedDict


class OpenAPIInfo(TypedDict):
    version: str
    title: str


class OpenAPIExternalDocs(TypedDict):
    description: str
    url: str


class OpenAPIRequestBody(TypedDict):
    required: bool


class OpenAPIPath(TypedDict):
    operationId: str
    summary: str
    description: str
    externalDocs: OpenAPIExternalDocs
    tags: list[str]
    security: list[dict[str, list[Any]]]


class OpenAPI(TypedDict):
    openapi: str
    info: OpenAPIInfo
    externalDocs: OpenAPIExternalDocs
    paths: dict[str, dict[Literal['post', 'get'], OpenAPIPath]]
