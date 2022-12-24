from importlib import import_module
from typing import Optional, Union


class APIError(Exception):
    """APIのエラー"""
    def __init__(self, data: Union[dict, str], status: int):
        self.raw: Union[dict, str] = data
        self.status: int = status
        self.code: Optional[str] = None
        self.id: Optional[str] = None
        self.message: Optional[str] = None
        if isinstance(data, dict):
            error = data.get("error", {})
            self.code: Optional[str] = error.get("code", "")
            self.id: Optional[str] = error.get("id")
            self.message: Optional[str] = error.get("message", "")
        super().__init__(self.message or self.raw)

    def raise_error(self):
        if not self.code:
            raise self
        if value := getattr(
            import_module("mipac.errors.errors"),
            "".join([i.capitalize() for i in self.code.split("_")]) + "Error",
            None,
        ):
            raise value(self.raw, self.status)
        else:
            raise self


class NotExistRequiredData(Exception):
    """クラスの中に必要なデータが不足している"""


class ParameterError(Exception):
    """引数に関するエラー"""
