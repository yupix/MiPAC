"""汎用的な型定義を行うモジュールです。"""

from typing import TypedDict


class IID(TypedDict):
    """IDを表す型"""

    id: str
