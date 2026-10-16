from datetime import datetime

from mipac.utils.format import remove_dict_empty, str_to_datetime, upper_to_lower


def test_upper_to_lower_converts_nested_keys():
    data = {"createdAt": 1, "user": {"avatarUrl": "x"}, "files": [{"fileId": 1}, "raw"]}
    assert upper_to_lower(data) == {
        "created_at": 1,
        "user": {"avatar_url": "x"},
        "files": [{"file_id": 1}, "raw"],
    }


def test_upper_to_lower_nest_false_keeps_inner_keys():
    assert upper_to_lower({"user": {"avatarUrl": "x"}}, nest=False) == {"user": {"avatarUrl": "x"}}


def test_upper_to_lower_replace_list():
    assert upper_to_lower({"id": "1"}, replace_list={"id": "note_id"}) == {"note_id": "1"}


def test_remove_dict_empty_keeps_ignored_keys():
    assert remove_dict_empty({"a": None, "b": 0, "c": None}, ignore_keys=["c"]) == {
        "b": 0,
        "c": None,
    }


def test_str_to_datetime():
    assert str_to_datetime("2024-01-02T03:04:05.678Z") == datetime(2024, 1, 2, 3, 4, 5, 678000)
