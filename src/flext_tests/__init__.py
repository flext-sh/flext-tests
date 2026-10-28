# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        x,
    )

    from flext_tests.__version__ import (
        FlextTestsVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_tests._cli import FlextTestsCliDocker
    from flext_tests._config import FlextTestsConfig, FlextTestsConfigNamespace, config
    from flext_tests._docker import FlextTestsDockerSurface
    from flext_tests._settings import FlextTestsSettings, settings
    from flext_tests.api import FlextTests, api
    from flext_tests.base import FlextTestsServiceBase, s
    from flext_tests.case import FlextTestsCase
    from flext_tests.cli import FlextTestsCli
    from flext_tests.constants import FlextTestsConstants, c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.models import FlextTestsModels, m
    from flext_tests.protocols import FlextTestsProtocols, p
    from flext_tests.pytest_bootstrap import install_local_packages
    from flext_tests.tmatchers import FlextTestsUtilitiesMatchers, tm
    from flext_tests.typings import FlextTestsTypes, t
    from flext_tests.utilities import (
        FlextTestsUtilities,
        FlextTestsUtilitiesFixturesDSL,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextTests",
    "FlextTestsCase",
    "FlextTestsCli",
    "FlextTestsCliDocker",
    "FlextTestsConfig",
    "FlextTestsConfigNamespace",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDockerSurface",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsUtilitiesFixturesDSL",
    "FlextTestsUtilitiesMatchers",
    "FlextTestsVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTests": ".api",
        "FlextTestsCase": ".case",
        "FlextTestsCli": ".cli",
        "FlextTestsCliDocker": "._cli_docker",
        "FlextTestsConfig": "._config",
        "FlextTestsConfigNamespace": "._config",
        "FlextTestsConstants": ".constants",
        "FlextTestsDocker": ".docker",
        "FlextTestsDockerSurface": "._docker_surface",
        "FlextTestsDomains": ".domains",
        "FlextTestsFiles": ".files",
        "FlextTestsUtilitiesFixturesDSL": ".utilities",
        "FlextTestsUtilitiesMatchers": ".tmatchers",
        "FlextTestsModels": ".models",
        "FlextTestsProtocols": ".protocols",
        "FlextTestsServiceBase": ".base",
        "FlextTestsSettings": "._settings",
        "FlextTestsTypes": ".typings",
        "FlextTestsUtilities": ".utilities",
        "FlextTestsVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "api": ".api",
        "build_lazy_import_map": "flext_cli",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_cli",
        "cli": "flext_cli",
        "config": "._config",
        "core": "flext_cli",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "install_lazy_exports": "flext_cli",
        "install_local_packages": ".pytest_bootstrap",
        "lazy": "flext_cli",
        "lazy_getattr": "flext_cli",
        "lazy_member": "flext_cli",
        "m": ".models",
        "main": "flext_cli",
        "merge_lazy_imports": "flext_cli",
        "normalize_lazy_imports": "flext_cli",
        "p": ".protocols",
        "r": "flext_cli",
        "resolve_lazy_members": "flext_cli",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "td": ".domains",
        "tf": ".files",
        "tk": ".docker",
        "tm": ".tmatchers",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_tests.__version__ import __version__
