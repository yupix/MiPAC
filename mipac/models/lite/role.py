from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mipac.types.roles import IPartialRole

if TYPE_CHECKING:
    from mipac.manager.admins.roles import AdminRolesModelManager
    from mipac.manager.client import ClientManager


class PartialRole[T: IPartialRole]:
    def __init__(self, role_data: T, *, client: ClientManager) -> None:
        self._raw_role: T = role_data
        self.__client = client

    @property
    def id(self) -> str:
        return self._raw_role["id"]

    @property
    def name(self) -> str:
        return self._raw_role["name"]

    @property
    def color(self) -> str | None:
        return self._raw_role["color"]

    @property
    def icon_url(self) -> str | None:
        return self._raw_role["icon_url"]

    @property
    def description(self) -> str:
        return self._raw_role["description"]

    @property
    def is_moderator(self) -> bool:
        return self._raw_role["is_moderator"]

    @property
    def is_administrator(self) -> bool:
        return self._raw_role["is_administrator"]

    @property
    def display_order(self) -> int:
        return self._raw_role["display_order"]

    @property
    def api(self) -> AdminRolesModelManager:
        return self.__client.admin.create_roles_model_manager(self.id)

    def _get(self, key: str) -> Any | None:
        return self._raw_role.get(key)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialRole) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
