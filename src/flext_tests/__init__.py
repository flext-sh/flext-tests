# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_tests.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_tests import services
    from flext_tests._config import FlextTestsConfig, config
    from flext_tests._settings import FlextTestsSettings, settings
    from flext_tests.api import FlextTests, api
    from flext_tests.base import FlextTestsServiceBase, s
    from flext_tests.case import FlextTestsCase
    from flext_tests.cli import FlextTestsCli
    from flext_tests.constants import FlextTestsConstants, c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.enforcement_plugin import SLOW_TIMEOUT_INI_OPTION
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.kube import FlextTestsKube
    from flext_tests.models import FlextTestsModels, m
    from flext_tests.protocols import FlextTestsProtocols, p
    from flext_tests.pytest_bootstrap import install_local_packages
    from flext_tests.tmatchers import FlextTestsMatchersUtilities, tm
    from flext_tests.typings import FlextTestsTypes, t
    from flext_tests.utilities import (
        FlextTestsFixturesDSLMixin,
        FlextTestsModuleGovernanceMixin,
        FlextTestsUtilities,
        u,
    )


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
    "FlextTestsModuleGovernanceMixin",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
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
    "config",
    "d",
    "e",
    "h",
    "install_local_packages",
    "m",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextTestsConfig", "config"),
            "._settings": ("FlextTestsSettings", "settings"),
            ".api": ("FlextTests", "api"),
            ".base": ("FlextTestsServiceBase", "s"),
            ".case": ("FlextTestsCase",),
            ".cli": ("FlextTestsCli",),
            ".constants": ("FlextTestsConstants", "c"),
            ".docker": ("FlextTestsDocker", "tk"),
            ".domains": ("FlextTestsDomains", "td"),
            ".enforcement_plugin": ("SLOW_TIMEOUT_INI_OPTION",),
            ".files": ("FlextTestsFiles", "tf"),
            ".kube": ("FlextTestsKube",),
            ".models": ("FlextTestsModels", "m"),
            ".protocols": ("FlextTestsProtocols", "p"),
            ".pytest_bootstrap": ("install_local_packages",),
            ".services": ("services",),
            ".tmatchers": ("FlextTestsMatchersUtilities", "tm"),
            ".typings": ("FlextTestsTypes", "t"),
            ".utilities": (
                "FlextTestsFixturesDSLMixin",
                "FlextTestsModuleGovernanceMixin",
                "FlextTestsUtilities",
                "u",
            ),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
