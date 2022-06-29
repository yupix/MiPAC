from typing import TypedDict

__all__ = (
    'ActiveUsersChartPayload',
    'DriveLocalChartPayload',
    'DriveRemoteChartPayload',
    'DriveChartPayload',
)


class ActiveUsersChartPayload(TypedDict):
    read_write: list[int]
    read: list[int]
    write: list[int]
    registered_within_week: list[int]
    registered_within_month: list[int]
    registered_within_year: list[int]
    registered_outside_week: list[int]
    registered_outside_month: list[int]
    registered_outside_year: list[int]


class DriveLocalChartPayload(TypedDict):
    total_count: list[int]
    total_size: list[int]
    inc_count: list[int]
    inc_size: list[int]
    dec_count: list[int]
    dec_size: list[int]


class DriveRemoteChartPayload(TypedDict):
    total_count: list[int]
    total_size: list[int]
    inc_count: list[int]
    inc_size: list[int]
    dec_count: list[int]
    dec_size: list[int]


class DriveChartPayload(TypedDict):
    local: DriveLocalChartPayload
    remote: DriveRemoteChartPayload
