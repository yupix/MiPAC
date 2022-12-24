from typing import TypedDict

__all__ = (
    'IActiveUsersChart',
    'IDriveLocalChart',
    'IDriveRemoteChart',
    'IDriveChart',
)


class IActiveUsersChart(TypedDict):
    read_write: list[int]
    read: list[int]
    write: list[int]
    registered_within_week: list[int]
    registered_within_month: list[int]
    registered_within_year: list[int]
    registered_outside_week: list[int]
    registered_outside_month: list[int]
    registered_outside_year: list[int]


class IDriveLocalChart(TypedDict):
    total_count: list[int]
    total_size: list[int]
    inc_count: list[int]
    inc_size: list[int]
    dec_count: list[int]
    dec_size: list[int]


class IDriveRemoteChart(TypedDict):
    total_count: list[int]
    total_size: list[int]
    inc_count: list[int]
    inc_size: list[int]
    dec_count: list[int]
    dec_size: list[int]


class IDriveChart(TypedDict):
    local: IDriveLocalChart
    remote: IDriveRemoteChart
