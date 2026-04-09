# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from tests.constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c
    from tests.models import TestsFlextTestsModels, TestsFlextTestsModels as m
    from tests.protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p
    from tests.typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t
    from tests.utilities import TestsFlextTestsUtilities, TestsFlextTestsUtilities as u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextTestsConstants",),
        ".models": ("TestsFlextTestsModels",),
        ".protocols": ("TestsFlextTestsProtocols",),
        ".typings": ("TestsFlextTestsTypes",),
        ".utilities": ("TestsFlextTestsUtilities",),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
    },
    alias_groups={
        ".constants": (("c", "TestsFlextTestsConstants"),),
        ".models": (("m", "TestsFlextTestsModels"),),
        ".protocols": (("p", "TestsFlextTestsProtocols"),),
        ".typings": (("t", "TestsFlextTestsTypes"),),
        ".utilities": (("u", "TestsFlextTestsUtilities"),),
    },
)

__all__ = [
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
