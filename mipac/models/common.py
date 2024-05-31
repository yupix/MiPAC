"""汎用的なモデルを定義するモジュールです。"""

from mipac.types.common import IID


class ID:
    def __init__(self, *, raw_id: IID) -> None:
        self.__raw_id: IID = raw_id

    @property
    def id(self) -> str:
        """The id of the object"""
        return self.__raw_id["id"]
