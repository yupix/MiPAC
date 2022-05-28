from abc import ABC, abstractmethod

__all__ = ('AbstractModel',)


class AbstractModel(ABC):
    @property
    @abstractmethod
    def action(self):
        pass
