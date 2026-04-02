# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_utils,
        typings,
        utilities,
    )
    from tests.conftest import td, tf, tk, tm, tt
    from tests.constants import FlextTestsTestConstants, FlextTestsTestConstants as c
    from tests.models import FlextTestsTestModels, FlextTestsTestModels as m
    from tests.protocols import FlextTestsTestProtocols, FlextTestsTestProtocols as p
    from tests.test_utils import AssertionHelpers, T, assertion_helpers
    from tests.typings import FlextTestsTestTypes, FlextTestsTestTypes as t
    from tests.unit.flext_tests import (
        TestAssertExists,
        TestBatchOperations,
        TestContainerInfo,
        TestContainerStatus,
        TestCreateInStatic,
        TestFileInfo,
        TestFileInfoFromModels,
        TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot,
        TestFlextTestsDomains,
        TestFlextTestsFiles,
        TestFlextTestsFilesNewApi,
        TestFlextTestsMatchers,
        TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext,
        TestInfoWithContentMeta,
        TestShortAlias,
    )
    from tests.utilities import FlextTestsTestUtilities, FlextTestsTestUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "AssertionHelpers": "tests.test_utils",
    "FlextTestsTestConstants": "tests.constants",
    "FlextTestsTestModels": "tests.models",
    "FlextTestsTestProtocols": "tests.protocols",
    "FlextTestsTestTypes": "tests.typings",
    "FlextTestsTestUtilities": "tests.utilities",
    "T": "tests.test_utils",
    "TestAssertExists": "tests.unit.flext_tests.test_files",
    "TestBatchOperations": "tests.unit.flext_tests.test_files",
    "TestContainerInfo": "tests.unit.flext_tests.test_docker",
    "TestContainerStatus": "tests.unit.flext_tests.test_docker",
    "TestCreateInStatic": "tests.unit.flext_tests.test_files",
    "TestFileInfo": "tests.unit.flext_tests.test_files",
    "TestFileInfoFromModels": "tests.unit.flext_tests.test_files",
    "TestFlextTestsDocker": "tests.unit.flext_tests.test_docker",
    "TestFlextTestsDockerWorkerId": "tests.unit.flext_tests.test_docker",
    "TestFlextTestsDockerWorkspaceRoot": "tests.unit.flext_tests.test_docker",
    "TestFlextTestsDomains": "tests.unit.flext_tests.test_domains",
    "TestFlextTestsFiles": "tests.unit.flext_tests.test_files",
    "TestFlextTestsFilesNewApi": "tests.unit.flext_tests.test_files",
    "TestFlextTestsMatchers": "tests.unit.flext_tests.test_matchers",
    "TestFlextTestsUtilitiesFactory": "tests.unit.flext_tests.test_utilities",
    "TestFlextTestsUtilitiesResult": "tests.unit.flext_tests.test_utilities",
    "TestFlextTestsUtilitiesResultCompat": "tests.unit.flext_tests.test_utilities",
    "TestFlextTestsUtilitiesTestContext": "tests.unit.flext_tests.test_utilities",
    "TestInfoWithContentMeta": "tests.unit.flext_tests.test_files",
    "TestShortAlias": "tests.unit.flext_tests.test_files",
    "assertion_helpers": "tests.test_utils",
    "c": ("tests.constants", "FlextTestsTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "h": "flext_tests",
    "m": ("tests.models", "FlextTestsTestModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTestsTestProtocols"),
    "protocols": "tests.protocols",
    "r": "flext_tests",
    "s": "flext_tests",
    "t": ("tests.typings", "FlextTestsTestTypes"),
    "td": "tests.conftest",
    "test_utils": "tests.test_utils",
    "tf": "tests.conftest",
    "tk": "tests.conftest",
    "tm": "tests.conftest",
    "tt": "tests.conftest",
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTestsTestUtilities"),
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
