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
    text: Optional[str]
    file_id: Optional[str]
    width: Optional[int]
    height: Optional[int]
    note: Optional[str]
    detailed: Optional[bool]
    fn: Optional[Any]
    var: Optional[Any]
    event: Optional[Any]
    action: Optional[str]
    content: Optional[str]
    message: Optional[Any]
    primary: Optional[bool]
    inc: Optional[int]
    canvas_id: Optional[str]
    attach_canvas_image: Optional[bool]
    default: Optional[str]
    value: Optional[list[Any]]

    children: Optional['PageContentPayload']


class VariablePayload(TypedDict):
    id: str
    name: str
    type: str
    value: Optional[str]


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
    comment: Optional[str]
    folder_id: Optional[str]
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
    summary: Optional[str]
    hide_title_when_pinned: bool
    align_center: bool
    font: str
    script: str
    eye_catching_image_id: Optional[str]
    eye_catching_image: EyeCatchingImagePayload
    attached_files: list[AttachedFilePayload]
    liked_count: int
