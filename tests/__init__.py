# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli, core, d, e, h, lazy_attribute, main, r, services, x

    from flext_tests import (
        active_rules,
        api,
        config,
        discover_repository_root,
        install_local_packages,
        load_infra_report,
        s,
        settings,
        split_csv,
        td,
        tf,
        tk,
        tm,
        tv,
    )

    from . import integration, unit
    from .constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c
    from .models import TestsFlextTestsModels, TestsFlextTestsModels as m
    from .protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p
    from .typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t
    from .utilities import TestsFlextTestsUtilities, TestsFlextTestsUtilities as u


__all__: tuple[str, ...] = (
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "active_rules",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "discover_repository_root",
    "e",
    "h",
    "install_local_packages",
    "integration",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "split_csv",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("TestsFlextTestsConstants", "c"),
            ".integration": ("integration",),
            ".models": ("TestsFlextTestsModels", "m"),
            ".protocols": ("TestsFlextTestsProtocols", "p"),
            ".typings": ("TestsFlextTestsTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextTestsUtilities", "u"),
            "flext_cli": (
                "cli",
                "core",
                "d",
                "e",
                "h",
                "lazy_attribute",
                "main",
                "r",
                "services",
                "x",
            ),
            "flext_tests": (
                "active_rules",
                "api",
                "config",
                "discover_repository_root",
                "install_local_packages",
                "load_infra_report",
                "s",
                "settings",
                "split_csv",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
