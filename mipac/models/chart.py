from mipac.types.chart import (
    IActiveUsersChart,
    IDriveChart,
    IDriveLocalChart,
    IDriveRemoteChart,
)


class ActiveUsersChart:
    __slots__ = ('__data',)

    def __init__(self, data: IActiveUsersChart):
        self.__data = data

    @property
    def read_write(self) -> list[int]:
        return self.__data['read_write']

    @property
    def read(self) -> list[int]:
        return self.__data['read']

    @property
    def write(self) -> list[int]:
        return self.__data['write']

    @property
    def registered_within_week(self) -> list[int]:
        return self.__data['registered_within_week']

    @property
    def registered_within_month(self) -> list[int]:
        return self.__data['registered_within_month']

    @property
    def registered_within_year(self) -> list[int]:
        return self.__data['registered_within_year']

    @property
    def registered_outside_week(self) -> list[int]:
        return self.__data['registered_outside_week']

    @property
    def registered_outside_month(self) -> list[int]:
        return self.__data['registered_outside_month']

    @property
    def registered_outside_year(self) -> list[int]:
        return self.__data['registered_outside_year']


class DriveLocalChart:
    __slots__ = ('__data',)

    def __init__(self, data: IDriveLocalChart):
        self.__data = data

    @property
    def total_count(self) -> list[int]:
        return self.__data['total_count']

    @property
    def total_size(self) -> list[int]:
        return self.__data['total_size']

    @property
    def inc_count(self) -> list[int]:
        return self.__data['inc_count']

    @property
    def inc_size(self) -> list[int]:
        return self.__data['inc_size']

    @property
    def dec_count(self) -> list[int]:
        return self.__data['dec_count']

    @property
    def dec_size(self) -> list[int]:
        return self.__data['dec_size']


class DriveRemoteChart:
    __slots__ = ('__data',)

    def __init__(self, data: IDriveRemoteChart):
        self.__data: IDriveRemoteChart = data

    @property
    def total_count(self) -> list[int]:
        return self.__data['total_count']

    @property
    def total_size(self) -> list[int]:
        return self.__data['total_size']

    @property
    def inc_count(self) -> list[int]:
        return self.__data['inc_count']

    @property
    def inc_size(self) -> list[int]:
        return self.__data['inc_size']

    @property
    def dec_count(self) -> list[int]:
        return self.__data['dec_count']

    @property
    def dec_size(self) -> list[int]:
        return self.__data['dec_size']


class DriveChart:
    __slots__ = ('__data',)

    def __init__(self, data: IDriveChart):
        self.__data: IDriveChart = data

    @property
    def local(self) -> DriveLocalChart:
        return DriveLocalChart(self.__data['local'])

    @property
    def remote(self) -> DriveRemoteChart:
        return DriveRemoteChart(self.__data['remote'])
