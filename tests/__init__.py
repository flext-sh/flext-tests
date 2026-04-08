# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import TestsFlextTestsModels, TestsFlextTestsModels as m

    protocols = _tests_protocols
    import tests.test_utils as _tests_test_utils
    from tests.protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p

    test_utils = _tests_test_utils
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t

    utilities = _tests_utilities
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
