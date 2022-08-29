from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.core.models.chat import RawChat
from mipac.core.models.drive import RawFolder
from mipac.core.models.instance import RawInstance
from mipac.models.chat import Chat
from mipac.models.drive import Folder
from mipac.models.instance import Instance
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

    def new_instance(self, raw_instance: RawInstance) -> Instance:
        return Instance(raw_instance, client=self._client)

    def new_chat(self, raw_chat: RawChat) -> Chat:
        return Chat(raw_chat, client=self._client)

    def create_user_instance(self, raw_user: RawUser) -> UserDetailed:
        return UserDetailed(raw_user, client=self._client)

    def new_follow_request(self, raw_follow_request: Any) -> FollowRequest:
        return FollowRequest(raw_follow_request)

    def new_folder(self, raw_folder: RawFolder) -> Folder:
        return Folder(raw_folder, client=self._client)
