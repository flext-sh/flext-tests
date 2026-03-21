# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes


if TYPE_CHECKING:
    from flext_tests import d, e, h, r, s, x

    from .conftest import td, tf, tk, tm, tt
    from .constants import TestsFlextTestsConstants, TestsFlextTestsConstants as c
    from .models import TestsFlextTestsModels, TestsFlextTestsModels as m
    from .protocols import TestsFlextTestsProtocols, TestsFlextTestsProtocols as p
    from .test_utils import AssertionHelpers, T, assertion_helpers
    from .typings import TestsFlextTestsTypes, TestsFlextTestsTypes as t
    from .unit.flext_tests.test_docker import (
        TestContainerInfo,
        TestContainerStatus,
        TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot,
    )
    from .unit.flext_tests.test_domains import TestFlextTestsDomains
    from .unit.flext_tests.test_files import (
        TestAssertExists,
        TestBatchOperations,
        TestCreateInStatic,
        TestFileInfo,
        TestFileInfoFromModels,
        TestFlextTestsFiles,
        TestFlextTestsFilesNewApi,
        TestInfoWithContentMeta,
        TestShortAlias,
    )
    from .unit.flext_tests.test_matchers import TestFlextTestsMatchers
    from .unit.flext_tests.test_utilities import (
        TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext,
    )
    from .utilities import TestsFlextTestsUtilities, TestsFlextTestsUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AssertionHelpers": ("tests.test_utils", "AssertionHelpers"),
    "T": ("tests.test_utils", "T"),
    "TestAssertExists": ("tests.unit.flext_tests.test_files", "TestAssertExists"),
    "TestBatchOperations": ("tests.unit.flext_tests.test_files", "TestBatchOperations"),
    "TestContainerInfo": ("tests.unit.flext_tests.test_docker", "TestContainerInfo"),
    "TestContainerStatus": (
        "tests.unit.flext_tests.test_docker",
        "TestContainerStatus",
    ),
    "TestCreateInStatic": ("tests.unit.flext_tests.test_files", "TestCreateInStatic"),
    "TestFileInfo": ("tests.unit.flext_tests.test_files", "TestFileInfo"),
    "TestFileInfoFromModels": (
        "tests.unit.flext_tests.test_files",
        "TestFileInfoFromModels",
    ),
    "TestFlextTestsDocker": (
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDocker",
    ),
    "TestFlextTestsDockerWorkerId": (
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDockerWorkerId",
    ),
    "TestFlextTestsDockerWorkspaceRoot": (
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDockerWorkspaceRoot",
    ),
    "TestFlextTestsDomains": (
        "tests.unit.flext_tests.test_domains",
        "TestFlextTestsDomains",
    ),
    "TestFlextTestsFiles": ("tests.unit.flext_tests.test_files", "TestFlextTestsFiles"),
    "TestFlextTestsFilesNewApi": (
        "tests.unit.flext_tests.test_files",
        "TestFlextTestsFilesNewApi",
    ),
    "TestFlextTestsMatchers": (
        "tests.unit.flext_tests.test_matchers",
        "TestFlextTestsMatchers",
    ),
    "TestFlextTestsUtilitiesFactory": (
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesFactory",
    ),
    "TestFlextTestsUtilitiesResult": (
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesResult",
    ),
    "TestFlextTestsUtilitiesResultCompat": (
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesResultCompat",
    ),
    "TestFlextTestsUtilitiesTestContext": (
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesTestContext",
    ),
    "TestInfoWithContentMeta": (
        "tests.unit.flext_tests.test_files",
        "TestInfoWithContentMeta",
    ),
    "TestShortAlias": ("tests.unit.flext_tests.test_files", "TestShortAlias"),
    "TestsFlextTestsConstants": ("tests.constants", "TestsFlextTestsConstants"),
    "TestsFlextTestsModels": ("tests.models", "TestsFlextTestsModels"),
    "TestsFlextTestsProtocols": ("tests.protocols", "TestsFlextTestsProtocols"),
    "TestsFlextTestsTypes": ("tests.typings", "TestsFlextTestsTypes"),
    "TestsFlextTestsUtilities": ("tests.utilities", "TestsFlextTestsUtilities"),
    "assertion_helpers": ("tests.test_utils", "assertion_helpers"),
    "c": ("tests.constants", "TestsFlextTestsConstants"),
    "d": ("flext_tests", "d"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "m": ("tests.models", "TestsFlextTestsModels"),
    "p": ("tests.protocols", "TestsFlextTestsProtocols"),
    "r": ("flext_tests", "r"),
    "s": ("flext_tests", "s"),
    "t": ("tests.typings", "TestsFlextTestsTypes"),
    "td": ("tests.conftest", "td"),
    "tf": ("tests.conftest", "tf"),
    "tk": ("tests.conftest", "tk"),
    "tm": ("tests.conftest", "tm"),
    "tt": ("tests.conftest", "tt"),
    "u": ("tests.utilities", "TestsFlextTestsUtilities"),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "AssertionHelpers",
    "T",
    "TestAssertExists",
    "TestBatchOperations",
    "TestContainerInfo",
    "TestContainerStatus",
    "TestCreateInStatic",
    "TestFileInfo",
    "TestFileInfoFromModels",
    "TestFlextTestsDocker",
    "TestFlextTestsDockerWorkerId",
    "TestFlextTestsDockerWorkspaceRoot",
    "TestFlextTestsDomains",
    "TestFlextTestsFiles",
    "TestFlextTestsFilesNewApi",
    "TestFlextTestsMatchers",
    "TestFlextTestsUtilitiesFactory",
    "TestFlextTestsUtilitiesResult",
    "TestFlextTestsUtilitiesResultCompat",
    "TestFlextTestsUtilitiesTestContext",
    "TestInfoWithContentMeta",
    "TestShortAlias",
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "assertion_helpers",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tt",
    "u",
    "x",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
