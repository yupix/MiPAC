from importlib import import_module
from typing import Union


class APIError(Exception):
    """APIのエラー"""

    def __init__(self, data: Union[dict, str], status: int):
        self.raw: Union[dict, str] = data
        self.status: int = status
        self.code: str | None = None
        self.id: str | None = None
        self.message: str | None = None
        if isinstance(data, dict):
            error = data.get('error', {})
            if isinstance(error, dict):
                self.code: str | None = error.get('code', '')
                self.id: str | None = error.get('id')
                self.message: str | None = error.get('message', '')
        super().__init__(self.message or self.raw)

    def raise_error(self):
        if not self.code:
            raise self
        if value := getattr(
            import_module('mipac.errors.errors'),
            ''.join([i.capitalize() for i in self.code.split('_')]) + 'Error',
            None,
        ):
            raise value(self.raw, self.status)
        else:
            raise self


class NotExistRequiredData(Exception):
    """クラスの中に必要なデータが不足している"""


class ParameterError(Exception):
    """引数に関するエラー"""


class NotSupportVersion(Exception):
    """サポートされていないバージョンのインスタンス"""
