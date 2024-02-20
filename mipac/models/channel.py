from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.note import Note
from mipac.types.channel import IChannel
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager import ClientManager
    from mipac.manager.channel import ClientChannelManager


class Channel:
    def __init__(self, raw_channel: IChannel, *, client: ClientManager) -> None:
        self._raw_channel: IChannel = raw_channel
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        """チャンネルID

        Returns
        -------
        str
        """
        return self._raw_channel["id"]

    @property
    def created_at(self) -> datetime:
        """チャンネルが作成された日時

        Returns
        -------
        datetime
        """
        return str_to_datetime(self._raw_channel["created_at"])

    @property
    def last_noted_at(self) -> datetime | None:
        """チャンネルに最後にノートが投稿された日時

        Returns
        -------
        datetime | None
        """
        last_noted_at = self._raw_channel.get("last_noted_at")
        return str_to_datetime(last_noted_at) if last_noted_at else None

    @property
    def name(self) -> str:
        """チャンネル名

        Returns
        -------
        str
        """
        return self._raw_channel["name"]

    @property
    def description(self) -> str | None:
        """チャンネルの説明

        Returns
        -------
        str | None
        """
        return self._raw_channel["description"]

    @property
    def user_id(self) -> str | None:
        """チャンネルを作成したユーザーのID

        Returns
        -------
        str | None
        """
        return self._raw_channel["user_id"]

    @property
    def banner_url(self) -> str | None:
        """チャンネルのバナー画像URL

        Returns
        -------
        str | None
        """
        return self._raw_channel["banner_url"]

    @property
    def pinned_note_ids(self) -> list[str]:
        """ピン留めされているノートのIDのリスト

        Returns
        -------
        list[str]
        """
        return self._raw_channel["pinned_note_ids"]

    @property
    def color(self) -> str:
        """チャンネルの色

        Returns
        -------
        str
        """
        return self._raw_channel["color"]

    @property
    def is_archived(self) -> bool:
        """チャンネルがアーカイブされているかどうか

        Returns
        -------
        bool
        """
        return self._raw_channel["is_archived"]

    @property
    def users_count(self) -> int:
        """チャンネルに参加しているユーザー数

        Returns
        -------
        int
        """
        return self._raw_channel["users_count"]

    @property
    def notes_count(self) -> int:
        """チャンネル内のノート数

        Returns
        -------
        int
        """
        return self._raw_channel["notes_count"]

    @property
    def is_sensitive(self) -> bool:
        """チャンネルがセンシティブかどうか

        Returns
        -------
        bool
        """
        return self._raw_channel["is_sensitive"]

    @property
    def allow_renote_to_external(self) -> bool:
        """外部へのリノートを許可するかどうか

        Returns
        -------
        bool
        """
        return self._raw_channel["allow_renote_to_external"]

    @property
    def is_following(self) -> bool | None:
        """自身がフォローしているかどうか

        Returns
        -------
        bool
        """
        return self._raw_channel.get("is_following")

    @property
    def is_favorited(self) -> bool | None:
        """自身がお気に入り登録しているかどうか

        Returns
        -------
        bool
        """
        return self._raw_channel.get("is_favorited")

    @property
    def pinned_notes(self) -> list[Note]:
        """ピン留めされているノートのリスト

        Returns
        -------
        list[Note]
        """
        return [
            Note(note, client=self.__client) for note in self._raw_channel.get("pinned_notes", [])
        ]

    @property
    def api(self) -> ClientChannelManager:
        """チャンネルに関するAPIを利用するためのクライアント

        Returns
        -------
        ClientChannelManager
        """
        return self.__client._create_client_channel_manager(channel_id=self.id)

    def _get(self, key: str) -> Any | None:
        return self._raw_channel.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Channel) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
