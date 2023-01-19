from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mipac.types.user import IUserDetailed


class IModerationLog(TypedDict):
    id: str
    created_at: str
    type: str
    info: dict  # TODO: これ何?
    user_id: str
    user: IUserDetailed


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
