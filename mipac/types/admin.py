from __future__ import annotations

from typing import TypedDict

from mipac.types.user import IUserDetailedNotMeSchema


class IUserIP(TypedDict):
    ip: str
    created_at: str


class IIndexStat(TypedDict):
    schemaname: str
    tablename: str
    indexname: str
    tablespace: str | None
    indexdef: str


class ITableStats(TypedDict):
    count: int
    size: int


class IModerationLog(TypedDict):
    id: str
    created_at: str
    type: str
    info: dict  # TODO: これ何?
    user_id: str
    user: IUserDetailedNotMeSchema


class IServerInfoCpu(TypedDict):
    models: str
    cores: int


class IServerInfoMem(TypedDict):
    total: int


class IServerInfoFs(TypedDict):
    total: int
    used: int


class IServerInfoNet(TypedDict):
    interface: str


class IServerInfo(TypedDict):
    machine: str
    os: str
    node: str
    psql: str
    cpu: IServerInfoCpu
    mem: IServerInfoMem
    fs: IServerInfoFs
    net: IServerInfoNet
