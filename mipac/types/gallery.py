from typing import NotRequired, TypedDict

from mipac.types.drive import IFile
from mipac.types.user import IPartialUser


class IGalleryPost(TypedDict):
    id: str
    created_at: str
    updated_at: str  # 更新が一度もない場合は created_atとほぼ同じものが入ってる
    user_id: str
    user: IPartialUser
    title: str
    description: str | None
    file_ids: list[str]
    files: list[IFile]
    tags: NotRequired[list[str]]  # Misskeyの今の実装では常に存在しない?
    is_sensitive: bool
    liked_count: int
    is_liked: NotRequired[bool]
