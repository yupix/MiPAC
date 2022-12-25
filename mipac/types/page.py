from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypedDict

from mipac.types.drive import IDriveFile
from mipac.types.user import ILiteUser

if TYPE_CHECKING:
    from mipac.types.drive import IFileProperties

__all__ = (
    'PageContentPayload',
    'VariablePayload',
    'PageFilePayload',
    'EyeCatchingImagePayload',
    'AttachedFilePayload',
    'PagePayload',
    'IPage',
)


class IPageRequired(TypedDict):
    id: str
    createdAt: str
    updatedAt: str
    userId: str
    user: ILiteUser
    content: list[dict[str, Any]]
    variables: list[dict[str, Any]]
    title: str
    name: str
    hideTitleWhenPinned: bool
    alignCenter: bool
    font: str
    script: str
    attachedFiles: Any
    likedCount: int


class IPage(IPageRequired, total=False):
    is_liked: bool
    eyeCatchingImageId: str
    eyeCatchingImage: IDriveFile
    summary: str


class PageContentPayload(TypedDict):
    id: str
    type: str
    text: str | None
    file_id: str | None
    width: int | None
    height: int | None
    note: str | None
    detailed: Optional[bool]
    fn: Optional[Any]
    var: Optional[Any]
    event: Optional[Any]
    action: str | None
    content: str | None
    message: Optional[Any]
    primary: Optional[bool]
    inc: int | None
    canvas_id: str | None
    attach_canvas_image: Optional[bool]
    default: str | None
    value: Optional[list[Any]]

    children: Optional['PageContentPayload']


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
    user: ILiteUser
    content: list[PageContentPayload]
    variable: list[VariablePayload]
    title: str
    name: str
    summary: str | None
    hide_title_when_pinned: bool
    align_center: bool
    font: str
    script: str
    eye_catching_image_id: str | None
    eye_catching_image: EyeCatchingImagePayload
    attached_files: list[AttachedFilePayload]
    liked_count: int
