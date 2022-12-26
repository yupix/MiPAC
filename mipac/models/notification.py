from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from mipac.models.lite.user import LiteUser
from mipac.models.note import Note

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions
    from mipac.manager.follow import FollowManager, FollowRequestManager
    from mipac.types.notification import INotification, IUserNf, \
        INoteNf, IPollEndNf, IReactionNf


class Notification:
    def __init__(
        self,
        notification: INotification,
        *,
        client: ClientActions,
    ) -> None:
        self.__notification: INotification = notification
        self.__client: ClientActions = client

    @property
    def id(self) -> str:
        return self.__notification['id']

    @property
    def type(self) -> str:
        return self.__notification['type']

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(
            self.__notification['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )

    @property
    def is_read(self) -> bool:
        return self.__notification['is_read']


class NotificationFollow(Notification):
    def __init__(
        self,
        notification: IUserNf,
        *,
        client: ClientActions,
    ) -> None:
        super().__init__(notification, client=client)
        self.__notification: IUserNf = notification
        self.__client: ClientActions = client

    @property
    def user(self) -> LiteUser:
        return LiteUser(
            self.__notification['user'], client=self.__client,
        )

    @property
    def user_id(self) -> str:
        return self.__notification['user_id']

    @property
    def api(self) -> FollowManager:
        return self.__client._create_user_instance(
            user=self.user
        ).follow


class NotificationFollowRequest(Notification):
    def __init__(
        self,
        notification: IUserNf,
        *,
        client: ClientActions,
    ) -> None:
        super().__init__(notification, client=client)
        self.__notification: IUserNf = notification
        self.__client: ClientActions = client

    @property
    def user(self) -> LiteUser:
        return LiteUser(
            self.__notification['user'], client=self.__client,
        )

    @property
    def user_id(self) -> str:
        return self.__notification['user_id']

    @property
    def api(self) -> FollowRequestManager:
        return self.__client._create_user_instance(
            user=self.user
        ).follow.request


class NotificationNote(Notification):
    def __init__(
        self,
        notification: INoteNf,
        *,
        client: ClientActions,
    ) -> None:
        super().__init__(notification, client=client)
        self.__notification: INoteNf = notification
        self.__client: ClientActions = client

    @property
    def user(self) -> LiteUser:
        return LiteUser(
            self.__notification['user'], client=self.__client,
        )

    @property
    def user_id(self) -> str:
        return self.__notification['user_id']

    @property
    def note(self) -> Note:
        return Note(
            self.__notification['note'], client=self.__client,
        )


class NotificationPollEnd(Notification):
    def __init__(
        self,
        notification: IPollEndNf,
        *,
        client: ClientActions,
    ) -> None:
        super().__init__(notification, client=client)
        self.__notification: IPollEndNf = notification
        self.__client: ClientActions = client

    @property
    def note(self) -> Note:
        return Note(
            self.__notification['note'], client=self.__client,
        )


class NotificationReaction(Notification):
    def __init__(
        self, reaction: IReactionNf, *, client: ClientActions
    ) -> None:
        super().__init__(reaction, client=client)
        self.__notification: IReactionNf = reaction
        self.__client: ClientActions = client

    @property
    def user(self) -> LiteUser:
        return LiteUser(self.__notification['user'], client=self.__client)

    @property
    def note(self) -> Note:
        return Note(self.__notification['note'], client=self.__client)

    @property
    def reaction(self) -> str:
        return self.__notification['reaction']
