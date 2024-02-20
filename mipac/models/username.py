from typing import Any
from mipac.types.username import IUsernameAvailable


class UsernameAvailable:
    def __init__(self, raw_username_available: IUsernameAvailable) -> None:
        self.__raw_username_available: IUsernameAvailable = raw_username_available

    @property
    def available(self) -> bool:
        return self.__raw_username_available["available"]

    def _get(self, key: str) -> Any | None:
        return self.__raw_username_available.get(key)
