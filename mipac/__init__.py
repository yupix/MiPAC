from ._version import get_versions

__title__ = 'mipac'
__author__ = 'yupix'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present yupix'
__author_email__ = 'yupi0982@outlook.jp'
__version__ = get_versions()['version']
del get_versions

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .abc import *  # noqa: F403, F401
from .models import *  # noqa: F403, F401

from . import _version
__version__ = _version.get_versions()['version']
