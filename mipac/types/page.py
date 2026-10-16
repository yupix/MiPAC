from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, NotRequired, TypedDict

from mipac.types.drive import IFile
from mipac.types.user import IPartialUser

if TYPE_CHECKING:
    from mipac.types.drive import IFileProperties

__all__ = (
    "PageContentPayload",
    "VariablePayload",
    "PageFilePayload",
    "EyeCatchingImagePayload",
    "AttachedFilePayload",
    "PagePayload",
    "IPage",
)


class IPageRequired(TypedDict):
    id: str
    created_at: str
    updated_at: str
    user_id: str
    user: IPartialUser
    content: list[dict[str, Any]]
    variables: list[dict[str, Any]]
    title: str
    name: str
    hide_title_when_pinned: bool
    align_center: bool
    font: Literal["serif", "sans-serif"]
    script: str
    attached_files: Any
    liked_count: int


class IPage(IPageRequired, total=False):
    is_liked: bool
    eye_catching_image_id: str | None
    eye_catching_image: IFile | None
    summary: str


class PageContentPayload(TypedDict):
    """Misskey Schema: `PageBlock`"""

    id: str
    type: Literal["text", "section", "image", "note"]
    text: NotRequired[str]  # type: text
    title: NotRequired[str]  # type: section
    children: NotRequired[list[PageContentPayload]]  # type: section
    file_id: NotRequired[str | None]  # type: image
    detailed: NotRequired[bool]  # type: note
    note: NotRequired[str | None]  # type: note


class VariablePayload(TypedDict):
    id: str
    name: str
    type: str
    value: str | None


class PageFilePayload(TypedDict):
    id: str
    created_at: str
    name: str
    type: str
    md5: str
    size: int
    is_sensitive: bool
    blurhash: str
    properties: IFileProperties
    url: str
    thumbnail_url: str
    comment: str | None
    folder_id: str | None
    folder: Any
    user_id: str
    user: Any


class EyeCatchingImagePayload(PageFilePayload):
    pass


class AttachedFilePayload(PageFilePayload):
    pass


class PagePayload(TypedDict):
    id: str
    created_at: str
    updated_at: str
    user_id: str
    user: IPartialUser
    content: list[PageContentPayload]
    variables: list[VariablePayload]
    title: str
    name: str
    summary: str | None
    hide_title_when_pinned: bool
    align_center: bool
    font: Literal["serif", "sans-serif"]
    script: str
    eye_catching_image_id: str | None
    eye_catching_image: EyeCatchingImagePayload
    attached_files: list[AttachedFilePayload]
    liked_count: int
