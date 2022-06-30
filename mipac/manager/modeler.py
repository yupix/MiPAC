from __future__ import annotations

from typing import TYPE_CHECKING

from mipac import File, User

if TYPE_CHECKING:
    from mipac.core import RawFile, RawUser
    from mipac.manager.client import ClientActions


class Modeler:
    """
    モデルを循環インポート無しでインスタンス化するためのクラスです
    """

    def __init__(self, client: ClientActions) -> None:
        self._client = client

    def create_user_instance(self, raw_user: RawUser) -> User:
        return User(raw_user, client=self._client)

    def create_file_instance(self, raw_file: RawFile) -> File:
        return File(raw_file, client=self._client)
