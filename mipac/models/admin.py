from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from mipac.models.user import UserDetailedNotMe, packed_user
from mipac.types.admin import (
    IIndexStat,
    IModerationLog,
    IServerInfo,
    IServerInfoCpu,
    IServerInfoFs,
    IServerInfoMem,
    IServerInfoNet,
    IUserIP,
)
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class UserIP:
    def __init__(self, user_ip: IUserIP) -> None:
        self.__user_ip: IUserIP = user_ip

    @property
    def ip(self) -> str:
        return self.__user_ip["ip"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__user_ip["created_at"])

    def _get(self, key: str) -> Any | None:
        return self.__user_ip.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, UserIP) and self.ip == __value.ip

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class IndexStat:
    def __init__(self, index_stat: IIndexStat) -> None:
        self.__index_stat: IIndexStat = index_stat

    @property
    def schemaname(self) -> str:
        return self.__index_stat["schemaname"]

    @property
    def tablename(self) -> str:
        return self.__index_stat["tablename"]

    @property
    def indexname(self) -> str:
        return self.__index_stat["indexname"]

    @property
    def tablespace(self) -> str | None:
        return self.__index_stat["tablespace"]

    @property
    def indexdef(self) -> str:
        return self.__index_stat["indexdef"]

    def _get(self, key: str) -> Any | None:
        return self.__index_stat.get(key)


class ModerationLog:
    def __init__(self, moderation_log: IModerationLog, *, client: ClientManager) -> None:
        self.__moderation_log: IModerationLog = moderation_log
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__moderation_log["id"]

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__moderation_log["created_at"])

    @property
    def type(self) -> str:
        return self.__moderation_log["type"]

    @property
    def info(self) -> dict:
        return self.__moderation_log["info"]

    @property
    def user_id(self) -> str:
        return self.__moderation_log["user_id"]

    @property
    def user(self) -> UserDetailedNotMe:
        return packed_user(self.__moderation_log["user"], client=self.__client)

    def _get(self, key: str) -> Any | None:
        return self.__moderation_log.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ModerationLog) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class ServerInfoCpu:
    def __init__(self, server_info_cpu: IServerInfoCpu) -> None:
        self.__server_info_cpu = server_info_cpu

    @property
    def models(self) -> str:
        return self.__server_info_cpu["models"]

    @property
    def cores(self) -> int:
        return self.__server_info_cpu["cores"]

    def _get(self, key: str) -> Any | None:
        return self.__server_info_cpu.get(key)


class ServerInfoMem:
    def __init__(self, server_info_mem: IServerInfoMem) -> None:
        self.__server_info_mem = server_info_mem

    @property
    def total(self) -> int:
        return self.__server_info_mem["total"]

    def _get(self, key: str) -> Any | None:
        return self.__server_info_mem.get(key)


class ServerInfoFs:
    def __init__(self, server_info_fs: IServerInfoFs) -> None:
        self.__server_info_fs = server_info_fs

    @property
    def total(self) -> int:
        return self.__server_info_fs["total"]

    @property
    def used(self) -> int:
        return self.__server_info_fs["used"]

    def _get(self, key: str) -> Any | None:
        return self.__server_info_fs.get(key)


class ServerInfoNet:
    def __init__(self, server_info_net: IServerInfoNet) -> None:
        self.__server_info_net = server_info_net

    @property
    def interface(self) -> str:
        return self.__server_info_net["interface"]

    def _get(self, key: str) -> Any | None:
        return self.__server_info_net.get(key)


class ServerInfo:
    def __init__(self, server_info: IServerInfo) -> None:
        self.__server_info = server_info

    @property
    def machine(self) -> str:
        return self.__server_info["machine"]

    @property
    def os(self) -> str:
        return self.__server_info["os"]

    @property
    def node(self) -> str:
        return self.__server_info["node"]

    @property
    def psql(self) -> str:
        return self.__server_info["psql"]

    @property
    def cpu(self) -> ServerInfoCpu:
        return ServerInfoCpu(self.__server_info["cpu"])

    @property
    def mem(self) -> ServerInfoMem:
        return ServerInfoMem(self.__server_info["mem"])

    @property
    def fs(self) -> ServerInfoFs:
        return ServerInfoFs(self.__server_info["fs"])

    @property
    def net(self) -> ServerInfoNet:
        return ServerInfoNet(self.__server_info["net"])

    def _get(self, key: str) -> Any | None:
        return self.__server_info.get(key)
