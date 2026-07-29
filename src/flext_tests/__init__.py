# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_infra import d as d
    from flext_infra import e as e
    from flext_infra import h as h
    from flext_infra import r as r
    from flext_infra import x as x

    from ._config import FlextTestsConfig as FlextTestsConfig
    from ._config import config as config
    from ._settings import FlextTestsSettings as FlextTestsSettings
    from ._settings import settings as settings
    from .base import FlextTestsCase as FlextTestsCase
    from .base import FlextTestsServiceBase as FlextTestsServiceBase

    s: type[FlextTestsServiceBase]
    from .constants import FlextTestsConstants as FlextTestsConstants

    c: type[FlextTestsConstants]
    from .docker import FlextTestsDocker as FlextTestsDocker
    from .docker import tk as tk
    from .domains import FlextTestsDomains as FlextTestsDomains
    from .domains import td as td
    from .files import FlextTestsFiles as FlextTestsFiles
    from .files import tf as tf
    from .models import FlextTestsModels as FlextTestsModels

    m: type[FlextTestsModels]
    from .protocols import FlextTestsProtocols as FlextTestsProtocols

    p: type[FlextTestsProtocols]
    from .tmatchers import FlextTestsMatchersUtilities as FlextTestsMatchersUtilities
    from .tmatchers import tm as tm
    from .typings import FlextTestsTypes as FlextTestsTypes

    t: type[FlextTestsTypes]
    from .utilities import FlextTestsUtilities as FlextTestsUtilities

    u: type[FlextTestsUtilities]
    from .validator import FlextTestsValidator as FlextTestsValidator
    from .validator import tv as tv

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextTestsConfig", "config"),
    "._settings": ("FlextTestsSettings", "settings"),
    ".base": ("FlextTestsCase", "FlextTestsServiceBase", "s"),
    ".constants": ("FlextTestsConstants", "c"),
    ".docker": ("FlextTestsDocker", "tk"),
    ".domains": ("FlextTestsDomains", "td"),
    ".files": ("FlextTestsFiles", "tf"),
    ".models": ("FlextTestsModels", "m"),
    ".protocols": ("FlextTestsProtocols", "p"),
    ".tmatchers": ("FlextTestsMatchersUtilities", "tm"),
    ".typings": ("FlextTestsTypes", "t"),
    ".utilities": ("FlextTestsUtilities", "u"),
    ".validator": ("FlextTestsValidator", "tv"),
    "flext_infra": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTestsCase",
    "FlextTestsConfig",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
