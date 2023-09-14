from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.models.lite.channel import ChannelLite
from mipac.types.channel import IChannel

if TYPE_CHECKING:
    from mipac.manager import ClientManager


class Channel(ChannelLite[IChannel]):
    def __init__(self, channel: IChannel, *, client: ClientManager) -> None:
        super().__init__(channel=channel, client=client)

    @property
    def has_unread_note(self) -> bool:
        return self._channel["has_unread_note"]

    @property
    def is_following(self) -> bool | None:
        return self._channel.get("is_following")

    @property
    def is_favorited(self) -> bool | None:
        return self._channel.get("is_favorited")
