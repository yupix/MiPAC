from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.core.models.emoji import RawEmoji

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('Emoji',)


class Emoji:
    def __init__(self, raw_data: RawEmoji, *, client: ClientActions):
        self._raw_data = raw_data
        self._client = client

    @property
    def id(self):
        return self._raw_data.id

    @property
    def aliases(self):
        return self._raw_data.aliases

    @property
    def name(self):
        return self._raw_data.name

    @property
    def category(self):
        return self._raw_data.category

    @property
    def host(self):
        return self._raw_data.host

    @property
    def url(self):
        return self._raw_data.url

    # @property
    # def action(self):
    #     return mi.framework.manager.ClientActions().emoji
