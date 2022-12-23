from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional

from mipac.exception import NotExistRequiredData, ParameterError
from mipac.http import HTTPClient, Route
from mipac.manager.note import NoteManager
from mipac.models.user import UserDetailed
from mipac.util import cache, check_multi_arg, remove_dict_empty

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.models.note import Note
    from mipac.models.lite.user import LiteUser

__all__ = ['UserActions']


class UserActions:
    def __init__(
        self,
        session: HTTPClient,
        client: ClientActions,
        user: Optional[LiteUser] = None,
    ):
        self.__session: HTTPClient = session
        self.__user: Optional[LiteUser] = user
        self.__client: ClientActions = client
        self.note: NoteManager = NoteManager(session=session, client=client)

    async def get_me(self) -> UserDetailed:
        """
        ログインしているユーザーの情報を取得します
        """

        res = await self.__session.request(Route('POST', '/api/i'), auth=True)
        return UserDetailed(res, client=self.__client)  # TODO: 自分用のクラスに変更する

    def get_profile_link(
        self,
        external: bool = True,
        protocol: Literal['http', 'https'] = 'https',
    ):
        if self.__user:
            host = (
                f'{protocol}://{self.__user.host}' or self.__session._url
                if external
                else self.__session._url
            )
            path = (
                f'/{self.__user.action.get_mention()}'
                if external is False
                else f'/@{self.__user.username}'
            )
            return host + path
        else:
            return None

    @cache(group='get_user')
    async def get(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserDetailed:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        UserDetailed
            ユーザー情報
        """

        field = remove_dict_empty(
            {'userId': user_id, 'username': username, 'host': host}
        )
        data = await self.__session.request(
            Route('POST', '/api/users/show'), json=field, auth=True, lower=True
        )
        return UserDetailed(data, client=self.__client)

    @cache
    async def fetch(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        host: Optional[str] = None,
    ) -> UserDetailed:
        """
        サーバーにアクセスし、ユーザーのプロフィールを取得します。基本的には get_userをお使いください。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        UserDetailed
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise ParameterError('user_id, usernameどちらかは必須です')

        field = remove_dict_empty(
            {'userId': user_id, 'username': username, 'host': host}
        )
        data = await self.__session.request(
            Route('POST', '/api/users/show'), json=field, auth=True, lower=True
        )
        return UserDetailed(data, client=self.__client)

    async def get_notes(
        self,
        user_id: Optional[str] = None,
        include_replies: bool = True,
        limit: int = 10,
        since_id: Optional[str] = None,
        until_id: Optional[str] = None,
        since_date: int = 0,
        until_date: int = 0,
        include_my_renotes: bool = True,
        with_files: bool = False,
        file_type: Optional[list[str]] = None,
        exclude_nsfw: bool = True,
    ) -> list[Note]:

        if check_multi_arg(user_id, self.__user):
            raise ParameterError('user_idがありません')

        user_id = user_id or self.__user and self.__user.id
        data = {
            'userId': user_id,
            'includeReplies': include_replies,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'sinceDate': since_date,
            'untilDate': until_date,
            'includeMyRenotes': include_my_renotes,
            'withFiles': with_files,
            'fileType': file_type,
            'excludeNsfw': exclude_nsfw,
        }
        res = await self.__session.request(
            Route('POST', '/api/users/notes'), json=data, auth=True, lower=True
        )
        return [Note(i, client=self.__client) for i in res]

    def get_mention(self, user: Optional[LiteUser] = None) -> str:
        """
        Get mention name of user.

        Parameters
        ----------
        user : Optional[User], default=None
            メンションを取得したいユーザーのオブジェクト

        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return (
            f'@{user.username}@{user.host}'
            if user.instance
            else f'@{user.username}'
        )
