from __future__ import annotations

from mipac.types.chart import (
    ActiveUsersChartPayload,
    DriveChartPayload,
    DriveLocalChartPayload,
    DriveRemoteChartPayload,
)

__all__ = (
    'RawActiveUsersChart',
    'RawDriveRemoteChart',
    'RawDriveLocalChart',
    'RawDriveChart',
)


class RawActiveUsersChart:
    __slots__ = (
        'read_write',
        'read',
        'write',
        'registered_within_week',
        'registered_within_month',
        'registered_within_year',
        'registered_outside_week',
        'registered_outside_month',
        'registered_outside_year',
    )

    def __init__(self, data: ActiveUsersChartPayload):
        self.read_write: list[int] = data['read_write']
        self.read: list[int] = data['read']
        self.write: list[int] = data['write']
        self.registered_within_week: list[int] = data['registered_within_week']
        self.registered_within_month: list[int] = data[
            'registered_within_month'
        ]
        self.registered_within_year: list[int] = data['registered_within_year']
        self.registered_outside_week: list[int] = data[
            'registered_outside_week'
        ]
        self.registered_outside_month: list[int] = data[
            'registered_outside_month'
        ]
        self.registered_outside_year: list[int] = data[
            'registered_outside_year'
        ]


class RawDriveLocalChart:
    __slots__ = (
        'total_count',
        'total_size',
        'inc_count',
        'inc_size',
        'dec_count',
        'dec_size',
    )

    def __init__(self, data: DriveLocalChartPayload):
        self.total_count: list[int] = data['total_count']
        self.total_size: list[int] = data['total_size']
        self.inc_count: list[int] = data['inc_count']
        self.inc_size: list[int] = data['inc_size']
        self.dec_count: list[int] = data['dec_count']
        self.dec_size: list[int] = data['dec_size']


class RawDriveRemoteChart:
    __slots__ = (
        'total_count',
        'total_size',
        'inc_count',
        'inc_size',
        'dec_count',
        'dec_size',
    )

    def __init__(self, data: DriveRemoteChartPayload):
        self.total_count: list[int] = data['total_count']
        self.total_size: list[int] = data['total_size']
        self.inc_count: list[int] = data['inc_count']
        self.inc_size: list[int] = data['inc_size']
        self.dec_count: list[int] = data['dec_count']
        self.dec_size: list[int] = data['dec_size']


class RawDriveChart:
    __slots__ = ('local', 'remote')

    def __init__(self, data: DriveChartPayload):
        self.local: RawDriveLocalChart = RawDriveLocalChart(data['local'])
        self.remote: RawDriveRemoteChart = RawDriveRemoteChart(data['remote'])
