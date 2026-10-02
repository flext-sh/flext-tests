# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, s, td, tf, tk, tm, x
    from tests import integration, unit
    from tests.constants import TestsFlextTestsConstants, c
    from tests.models import TestsFlextTestsModels, m
    from tests.protocols import TestsFlextTestsProtocols, p
    from tests.typings import TestsFlextTestsTypes, t
    from tests.utilities import TestsFlextTestsUtilities, u

__all__: tuple[str, ...] = (
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "api",
    "c",
    "d",
    "e",
    "h",
    "integration",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
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
            "flext_tests": (
                "api",
                "d",
                "e",
                "h",
                "r",
                "s",
                "td",
                "tf",
                "tk",
                "tm",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
