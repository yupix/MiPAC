MANAGER_TEMPLATE = """
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class {0}Manager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self):
        return\n
"""

ACTIONS_TEMPLATE = """
from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class {0}Actions(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client\n
"""

TEMPLATES = {'manager': MANAGER_TEMPLATE, 'actions': ACTIONS_TEMPLATE}
