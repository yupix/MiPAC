MANAGER_CLASS_NAME_TEMPLATE = '{0}Manager'
MANAGER_TEMPLATE = '''
from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient
from {1} import {2}

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager


class {0}(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    @property
    def action(self) -> {2}:
        return {2}(session=self.__session, client=self.__client)
'''

ACTIONS_CLASS_NAME_TEMPLATE = '{0}Actions'
ACTIONS_TEMPLATE = '''
from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.action import AbstractAction
from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.client import ClientManager


class {0}(AbstractAction):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client\n
'''

