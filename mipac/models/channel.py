from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

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
        return self._raw_channel["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._raw_channel["created_at"])

    @property
    def last_noted_at(self) -> datetime | None:
        last_noted_at = self._raw_channel.get("last_noted_at")
        return str_to_datetime(last_noted_at) if last_noted_at else None

    @property
    def name(self) -> str:
        return self._raw_channel["name"]

    @property
    def description(self) -> str | None:
        return self._raw_channel["description"]

    @property
    def user_id(self) -> str | None:
        return self._raw_channel["user_id"]

    @property
    def banner_url(self) -> str | None:
        return self._raw_channel["banner_url"]

    @property
    def pinned_note_ids(self) -> list[str]:
        return self._raw_channel["pinned_note_ids"]

    @property
    def color(self) -> str:
        return self._raw_channel["color"]

    @property
    def is_archived(self) -> bool:
        return self._raw_channel["is_archived"]

    @property
    def users_count(self) -> int:
        return self._raw_channel["users_count"]

    @property
    def notes_count(self) -> int:
        return self._raw_channel["notes_count"]

    @property
    def is_sensitive(self) -> bool:
        return self._raw_channel["is_sensitive"]

    @property
    def allow_renote_to_external(self) -> bool:
        return self._raw_channel["allow_renote_to_external"]

    @property
    def is_following(self) -> bool | None:
        return self._raw_channel.get("is_following")

    @property
    def is_favorited(self) -> bool | None:
        return self._raw_channel.get("is_favorited")

    @property
    def pinned_notes(self) -> list[Note]:
        return [
            Note(note, client=self.__client) for note in self._raw_channel.get("pinned_notes", [])
        ]

    @property
    def api(self) -> ClientChannelManager:
        return self.__client._create_client_channel_manager(channel_id=self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Channel) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
