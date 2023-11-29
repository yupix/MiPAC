from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.http import HTTPClient


__all__ = ("AbstractAction",)


class AbstractAction(ABC):
    @abstractmethod
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self._session = session
        self._client = client
