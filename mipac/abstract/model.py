from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


__all__ = ("AbstractModel",)


class AbstractModel(ABC):
    @abstractmethod
    def __init__(self, data: Any, *, client: ClientManager) -> None:
        pass
