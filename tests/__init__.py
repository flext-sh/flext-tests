# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from tests.constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c
    from tests.models import TestsFlextTestsModels, TestsFlextTestsModels as m
    from tests.protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p
    from tests.typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t
    from tests.utilities import TestsFlextTestsUtilities, TestsFlextTestsUtilities as u

    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
_LAZY_IMPORTS = {
    "TestsFlextTestsConstants": ("tests.constants", "TestsFlextTestsConstants"),
    "TestsFlextTestsModels": ("tests.models", "TestsFlextTestsModels"),
    "TestsFlextTestsProtocols": ("tests.protocols", "TestsFlextTestsProtocols"),
    "TestsFlextTestsTypes": ("tests.typings", "TestsFlextTestsTypes"),
    "TestsFlextTestsUtilities": ("tests.utilities", "TestsFlextTestsUtilities"),
    "c": ("tests.constants", "TestsFlextTestsConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextTestsModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "TestsFlextTestsProtocols"),
    "protocols": "tests.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextTestsTypes"),
    "test_utils": "tests.test_utils",
    "typings": "tests.typings",
    "u": ("tests.utilities", "TestsFlextTestsUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "t",
    "test_utils",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
