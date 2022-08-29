from __future__ import annotations

from typing import Any, TYPE_CHECKING

from mipac.models.user import FollowRequest, UserDetailed

if TYPE_CHECKING:
    from mipac.core import RawUser
    from mipac.manager.client import ClientActions


class Modeler:
    """
    モデルを循環インポート無しでインスタンス化するためのクラスです
    """

    def __init__(self, client: ClientActions) -> None:
        self._client = client

    def create_user_instance(self, raw_user: RawUser) -> UserDetailed:
        return UserDetailed(raw_user, client=self._client)

    def new_follow_request(self, raw_follow_request: Any) -> FollowRequest:
        return FollowRequest(raw_follow_request)
