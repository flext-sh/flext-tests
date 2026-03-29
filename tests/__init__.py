# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_tests import d, e, h, r, s, x
    from tests.conftest import td, tf, tk, tm, tt
    from tests.constants import FlextTestsTestConstants, FlextTestsTestConstants as c
    from tests.models import FlextTestsTestModels, FlextTestsTestModels as m
    from tests.protocols import FlextTestsTestProtocols, FlextTestsTestProtocols as p
    from tests.test_utils import AssertionHelpers, T, assertion_helpers
    from tests.typings import FlextTestsTestTypes, FlextTestsTestTypes as t
    from tests.unit.flext_tests.test_docker import (
        TestContainerInfo,
        TestContainerStatus,
        TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot,
    )
    from tests.unit.flext_tests.test_domains import TestFlextTestsDomains
    from tests.unit.flext_tests.test_files import (
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
    from tests.unit.flext_tests.test_matchers import TestFlextTestsMatchers
    from tests.unit.flext_tests.test_utilities import (
        TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext,
    )
    from tests.utilities import FlextTestsTestUtilities, FlextTestsTestUtilities as u

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "AssertionHelpers": ["tests.test_utils", "AssertionHelpers"],
    "FlextTestsTestConstants": ["tests.constants", "FlextTestsTestConstants"],
    "FlextTestsTestModels": ["tests.models", "FlextTestsTestModels"],
    "FlextTestsTestProtocols": ["tests.protocols", "FlextTestsTestProtocols"],
    "FlextTestsTestTypes": ["tests.typings", "FlextTestsTestTypes"],
    "FlextTestsTestUtilities": ["tests.utilities", "FlextTestsTestUtilities"],
    "T": ["tests.test_utils", "T"],
    "TestAssertExists": ["tests.unit.flext_tests.test_files", "TestAssertExists"],
    "TestBatchOperations": ["tests.unit.flext_tests.test_files", "TestBatchOperations"],
    "TestContainerInfo": ["tests.unit.flext_tests.test_docker", "TestContainerInfo"],
    "TestContainerStatus": ["tests.unit.flext_tests.test_docker", "TestContainerStatus"],
    "TestCreateInStatic": ["tests.unit.flext_tests.test_files", "TestCreateInStatic"],
    "TestFileInfo": ["tests.unit.flext_tests.test_files", "TestFileInfo"],
    "TestFileInfoFromModels": ["tests.unit.flext_tests.test_files", "TestFileInfoFromModels"],
    "TestFlextTestsDocker": ["tests.unit.flext_tests.test_docker", "TestFlextTestsDocker"],
    "TestFlextTestsDockerWorkerId": ["tests.unit.flext_tests.test_docker", "TestFlextTestsDockerWorkerId"],
    "TestFlextTestsDockerWorkspaceRoot": ["tests.unit.flext_tests.test_docker", "TestFlextTestsDockerWorkspaceRoot"],
    "TestFlextTestsDomains": ["tests.unit.flext_tests.test_domains", "TestFlextTestsDomains"],
    "TestFlextTestsFiles": ["tests.unit.flext_tests.test_files", "TestFlextTestsFiles"],
    "TestFlextTestsFilesNewApi": ["tests.unit.flext_tests.test_files", "TestFlextTestsFilesNewApi"],
    "TestFlextTestsMatchers": ["tests.unit.flext_tests.test_matchers", "TestFlextTestsMatchers"],
    "TestFlextTestsUtilitiesFactory": ["tests.unit.flext_tests.test_utilities", "TestFlextTestsUtilitiesFactory"],
    "TestFlextTestsUtilitiesResult": ["tests.unit.flext_tests.test_utilities", "TestFlextTestsUtilitiesResult"],
    "TestFlextTestsUtilitiesResultCompat": ["tests.unit.flext_tests.test_utilities", "TestFlextTestsUtilitiesResultCompat"],
    "TestFlextTestsUtilitiesTestContext": ["tests.unit.flext_tests.test_utilities", "TestFlextTestsUtilitiesTestContext"],
    "TestInfoWithContentMeta": ["tests.unit.flext_tests.test_files", "TestInfoWithContentMeta"],
    "TestShortAlias": ["tests.unit.flext_tests.test_files", "TestShortAlias"],
    "assertion_helpers": ["tests.test_utils", "assertion_helpers"],
    "c": ["tests.constants", "FlextTestsTestConstants"],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextTestsTestModels"],
    "p": ["tests.protocols", "FlextTestsTestProtocols"],
    "r": ["flext_tests", "r"],
    "s": ["flext_tests", "s"],
    "t": ["tests.typings", "FlextTestsTestTypes"],
    "td": ["tests.conftest", "td"],
    "tf": ["tests.conftest", "tf"],
    "tk": ["tests.conftest", "tk"],
    "tm": ["tests.conftest", "tm"],
    "tt": ["tests.conftest", "tt"],
    "u": ["tests.utilities", "FlextTestsTestUtilities"],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "AssertionHelpers",
    "FlextTestsTestConstants",
    "FlextTestsTestModels",
    "FlextTestsTestProtocols",
    "FlextTestsTestTypes",
    "FlextTestsTestUtilities",
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
