# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_infra import docs_main, infra, main
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, e, h, lazy_attribute, r, x

    from . import services
    from ._config import FlextTestsConfig, config
    from ._settings import FlextTestsSettings
    from .api import FlextTests, FlextTests as api
    from .base import FlextTestsCase, FlextTestsServiceBase, s
    from .cli import FlextTestsCli
    from .constants import FlextTestsConstants, c
    from .docker import FlextTestsDocker, tk
    from .domains import FlextTestsDomains, td
    from .enforcement import load_infra_report
    from .enforcement_plugin import SLOW_TIMEOUT_INI_OPTION
    from .files import FlextTestsFiles, tf
    from .kube import FlextTestsKube
    from .models import FlextTestsModels, m
    from .protocols import FlextTestsProtocols, p
    from .pytest_bootstrap import install_local_packages
    from .tmatchers import FlextTestsMatchersUtilities, tm
    from .typings import FlextTestsTypes, t
    from .utilities import FlextTestsFixturesDSLMixin, FlextTestsUtilities, u
    from .validator import FlextTestsValidator, FlextTestsValidator as tv
__all__: tuple[str, ...] = (
    "SLOW_TIMEOUT_INI_OPTION",
    "FlextTests",
    "FlextTestsCase",
    "FlextTestsCli",
    "FlextTestsConfig",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsFixturesDSLMixin",
    "FlextTestsKube",
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
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "docs_main",
    "e",
    "from_json",
    "h",
    "infra",
    "install_local_packages",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "to_json",
    "to_jsonable_python",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextTestsConfig", "config"),
            "._settings": ("FlextTestsSettings",),
            ".api": ("FlextTests", "api"),
            ".base": ("FlextTestsCase", "FlextTestsServiceBase", "s"),
            ".cli": ("FlextTestsCli",),
            ".constants": ("FlextTestsConstants", "c"),
            ".docker": ("FlextTestsDocker", "tk"),
            ".domains": ("FlextTestsDomains", "td"),
            ".enforcement": ("load_infra_report",),
            ".enforcement_plugin": ("SLOW_TIMEOUT_INI_OPTION",),
            ".files": ("FlextTestsFiles", "tf"),
            ".kube": ("FlextTestsKube",),
            ".models": ("FlextTestsModels", "m"),
            ".protocols": ("FlextTestsProtocols", "p"),
            ".pytest_bootstrap": ("install_local_packages",),
            ".services": ("services",),
            ".tmatchers": ("FlextTestsMatchersUtilities", "tm"),
            ".typings": ("FlextTestsTypes", "t"),
            ".utilities": ("FlextTestsFixturesDSLMixin", "FlextTestsUtilities", "u"),
            ".validator": ("FlextTestsValidator", "tv"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "flext_infra": ("docs_main", "infra", "main"),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
