# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import integration as integration
    from . import unit as unit
    from flext_tests import FlextTestsConstants, d, e, h, r, s, td, tf, tk, tm, tv, x

    from .conftest import pytest_plugins
    from .constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c
    from .models import TestsFlextTestsModels, TestsFlextTestsModels as m
    from .protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p
    from .typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t
    from .utilities import TestsFlextTestsUtilities, TestsFlextTestsUtilities as u
__all__: tuple[str, ...] = (
    "FlextTestsConstants",
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "c",
    "d",
    "e",
    "h",
    "integration",
    "m",
    "p",
    "pytest_plugins",
    "r",
    "s",
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
            ".conftest": ("pytest_plugins",),
            ".constants": ("TestsFlextTestsConstants", "c"),
            ".integration": ("integration",),
            ".models": ("TestsFlextTestsModels", "m"),
            ".protocols": ("TestsFlextTestsProtocols", "p"),
            ".typings": ("TestsFlextTestsTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextTestsUtilities", "u"),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "s",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
