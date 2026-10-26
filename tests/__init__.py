# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        api,
        cli,
        config,
        d,
        e,
        h,
        install_local_packages,
        main,
        r,
        s,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )
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
    "cli",
    "config",
    "d",
    "e",
    "h",
    "install_local_packages",
    "m",
    "main",
    "p",
    "r",
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
        "TestsFlextTestsConstants": ".constants",
        "TestsFlextTestsModels": ".models",
        "TestsFlextTestsProtocols": ".protocols",
        "TestsFlextTestsTypes": ".typings",
        "TestsFlextTestsUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "cli": "flext_tests",
        "config": "flext_tests",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "install_local_packages": "flext_tests",
        "m": ".models",
        "main": "flext_tests",
        "p": ".protocols",
        "r": "flext_tests",
        "s": "flext_tests",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
