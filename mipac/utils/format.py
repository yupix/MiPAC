import re
from datetime import datetime
from typing import Any, Mapping

from mipac.utils.util import Missing


def snake_to_camel(snake_str: str, replace_list: dict[str, str]) -> str:
    components: list[str] = snake_str.split("_")
    for i in range(len(components)):
        if components[i] in replace_list:
            components[i] = replace_list[components[i]]
    return components[0] + "".join(x.title() for x in components[1:])


def convert_dict_keys_to_camel(
    data: Mapping[Any, Any], replace_list: dict[str, str] | None = None
) -> Mapping[Any, Any]:
    if replace_list is None:
        replace_list = {}
    new_dict = {}
    for key, value in data.items():
        new_key = snake_to_camel(key, replace_list)
        new_dict[new_key] = value
    return new_dict


def str_to_datetime(data: str, format: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> datetime:
    """
    Parameters
    ----------
    data : str
        datetimeに変更したい文字列
    format : str
        dataのフォーマット

    Returns
    -------
    datetime
        変換後のデータ
    """
    return datetime.strptime(data, format)


def remove_list_empty(data: list[Any]) -> list[Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    dict[str, Any]
        空のkeyがなくなったdict
    """
    return [k for k in data if k]


def remove_dict_empty(
    data: dict[str, Any], ignore_keys: list[str] | None = None
) -> dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict
    ignore_keys: list
        削除したくないkeyのリスト

    Returns
    -------
    _data: dict
        空のkeyがなくなったdict
    """
    _data = {}
    if ignore_keys is None:
        ignore_keys = []
    _data = {k: v for k, v in data.items() if v is not None or k in ignore_keys}
    return _data


def remove_dict_missing(data: dict[str, Any]) -> dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    _data: dict
        MISSINGのkeyがなくなったdict
    """
    _data = {}
    _data = {k: v for k, v in data.items() if isinstance(v, Missing) is False}
    return _data


def upper_to_lower(
    data: dict[str, Any],
    field: dict[str, Any] | None = None,
    nest: bool = True,
    replace_list: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Parameters
    ----------
    data: dict[str, Any]
        小文字にしたいkeyがあるdict
    field: dict[str, Any] | None, default=None
        謎
    nest: bool, default=True
        ネストされたdictのkeyも小文字にするか否か
    replace_list: dict[str, Any] | None, default=None
        dictのkey名を特定の物に置き換える

    Returns
    -------
    field : dict[str, Any]
        小文字になった, key名が変更されたdict
    """
    if data is None:
        return {}
    if replace_list is None:
        replace_list = {}

    if field is None:
        field = {}
    for attr in data:
        pattern = re.compile("[A-Z]")
        large = [i.group().lower() for i in pattern.finditer(attr)]
        result: list[Any | str] = [None] * (len(large + pattern.split(attr)))
        result[::2] = pattern.split(attr)
        result[1::2] = ["_" + i.lower() for i in large]
        default_key = "".join(result)
        if replaced_value := replace_list.get(attr):
            default_key = default_key.replace(attr, replaced_value)
        field[default_key] = data[attr]
        if isinstance(field[default_key], dict) and nest:
            field[default_key] = upper_to_lower(field[default_key])
        elif isinstance(field[default_key], list) and nest:
            field[default_key] = [
                upper_to_lower(i) if isinstance(i, dict) else i for i in field[default_key]
            ]
    return field


def str_lower(text: str):
    pattern = re.compile("[A-Z]")
    large = [i.group().lower() for i in pattern.finditer(text)]
    result: list[Any | str] = [None] * (len(large + pattern.split(text)))
    result[::2] = pattern.split(text)
    result[1::2] = ["_" + i.lower() for i in large]
    return "".join(result)


def bool_to_string(boolean: bool) -> str:
    """
    boolを小文字にして文字列として返します

    Parameters
    ----------
    boolean : bool
        変更したいbool値
    Returns
    -------
    true or false: str
        小文字になったbool文字列
    """
    return "true" if boolean else "false"
