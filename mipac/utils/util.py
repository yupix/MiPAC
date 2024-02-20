import functools
import json
import warnings
from datetime import datetime, timedelta
from typing import Any


try:
    import orjson  # type: ignore
except ModuleNotFoundError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True

if HAS_ORJSON:
    _from_json = orjson.loads  # type: ignore
else:
    _from_json = json.loads


class Missing:
    def __repr__(self) -> str:
        return "MISSING"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Missing)

    def __ne__(self, other: Any) -> bool:
        return not isinstance(other, Missing)


MISSING: Any = Missing()


class DeprecatedClass:
    def __init__(self, remove_in_version: str) -> None:
        self.remove_in_version = remove_in_version

    def __call__(self, cls):
        remove_in_version = self.remove_in_version

        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                warnings.simplefilter("always", DeprecationWarning)  # turn off filter
                warnings.warn(
                    "Call to deprecated class {}. (Remove will this class at v{})".format(
                        cls.__name__, remove_in_version
                    ),
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                warnings.simplefilter("default", DeprecationWarning)  # reset filter
                super().__init__(*args, **kwargs)

        return Wrapped


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def check_multi_arg(*args: Any) -> bool:
    """
    複数の値を受け取り値が存在するかをboolで返します

    Parameters
    ----------
    args : list
        確認したい変数のリスト

    Returns
    -------
    bool
        存在する場合はTrue, 存在しない場合はFalse
    """
    return bool([i for i in args if i])


class MiTime:
    def __init__(self, start: timedelta, end: datetime):
        self.start = start
        self.end = end


class Colors:
    def __init__(self) -> None:
        self.green = "\x1b[92;1m"
        self.reset = "\x1b[0m"


COLORS = Colors()
