from typing import Any, Literal, NotRequired, TypedDict


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
    requestBody: OpenAPIRequestBody


class OpenAPIComponentProperty(TypedDict):
    type: str | None
    format: NotRequired[str]
    items: NotRequired["OpenAPIComponentSchema"]


class OpenAPIComponentSchema(TypedDict):
    type: Literal["object"]
    properties: dict[str, OpenAPIComponentProperty]


class OpenAPIComponents(TypedDict):
    schemas: dict[str, OpenAPIComponentSchema]


class OpenAPI(TypedDict):
    openapi: str
    info: OpenAPIInfo
    externalDocs: OpenAPIExternalDocs
    paths: dict[str, dict[Literal['post', 'get'], OpenAPIPath]]
    components: OpenAPIComponents
