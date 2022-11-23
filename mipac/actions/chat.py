from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abc.action import AbstractAction
from mipac.exception import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.chat import ChatMessage
from mipac.types.chat import IChatMessage
from mipac.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class BaseChatAction(AbstractAction):
    def __init__(
        self,
        session: HTTPClient,
        client: ClientActions,
        *,
        user_id: str | None = None,
        message_id: str | None = None,
    ):
        self.__session = session
        self.__client = client
        self.__user_id = user_id
        self.__message_id = message_id

    async def read(self, message_id: str | None = None) -> bool:
        """
        指定したIdのメッセージを既読にします

        Parameters
        ----------
        message_id : str
            Message id

        Returns
        -------
        bool
            Success or Failure.
        """
        if check_multi_arg(message_id, self.__message_id) is False:
            raise ParameterError('message_idがありません')
        message_id = message_id or self.__message_id
        body = {'messageId': message_id}
        res: bool = await self.__session.request(
            Route('POST', '/api/messaging/messages/read'),
            json=body,
            auth=True,
            lower=True,
        )
        return res

    async def delete(self, message_id: str | None = None) -> bool:
        """
        指定したidのメッセージを削除します。

        Parameters
        ----------
        message_id : str
            Message id

        Returns
        -------
        bool
            Success or Failure.
        """

        if check_multi_arg(message_id, self.__message_id) is False:
            raise ParameterError('message_idがありません')

        message_id = message_id or self.__message_id
        body = {'messageId': f'{message_id}'}
        res: bool = await self.__session.request(
            Route('POST', '/api/messaging/messages/delete'),
            json=body,
            auth=True,
        )
        return bool(res)


class ChatAction(BaseChatAction):
    def __init__(
        self,
        session: HTTPClient,
        client: ClientActions,
        *,
        user_id: str | None = None,
        message_id: str | None = None,
    ):
        super().__init__(
            session, client, user_id=user_id, message_id=message_id
        )

    async def get_history(self, limit: int = 100, group: bool = True):
        """
        Get the chat history.

        Parameters
        ----------
        limit : int, default=100, max=100
            Number of items to retrieve, up to 100
        group : bool, default=True
            Whether to include group chat or not

        Returns
        -------
        list[ChatMessage]
            List of chat history
        """

        if limit > 100:
            raise ParameterError('limit must be greater than 100')

        args = {'limit': limit, 'group': group}
        data: list[IChatMessage] = await self.__session.request(
            Route('POST', '/api/messaging/history'), json=args, auth=True
        )
        return [ChatMessage(d, client=self.__client) for d in data]

    async def send(
        self,
        text: str | None = None,
        *,
        file_id: str | None = None,
        user_id: str | None = None,
        group_id: str | None = None,
    ) -> ChatMessage:
        """
        Send chat.

        Parameters
        ----------
        text : Optional[str], default=None
            Chat content
        file_id : Optional[str], default=None
            添付するファイルのID
        user_id : Optional[str], default=None
            送信するユーザーのID
        group_id : Optional[str], default=None
            Destination group id
        """
        user_id = user_id or self.__user_id
        data = {
            'userId': user_id,
            'groupId': group_id,
            'text': text,
            'fileId': file_id,
        }
        res = await self.__session.request(
            Route('POST', '/api/messaging/messages/create'),
            json=data,
            auth=True,
            lower=True,
        )
        return ChatMessage(res, client=self.__client)
