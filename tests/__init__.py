# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import d as d, e as e, h as h, r as r, s as s, x as x
    from tests import (
        conftest as conftest,
        constants as constants,
        models as models,
        protocols as protocols,
        test_utils as test_utils,
        typings as typings,
        utilities as utilities,
    )
    from tests.conftest import td as td, tf as tf, tk as tk, tm as tm, tt as tt
    from tests.constants import (
        FlextTestsTestConstants as FlextTestsTestConstants,
        FlextTestsTestConstants as c,
    )
    from tests.models import (
        FlextTestsTestModels as FlextTestsTestModels,
        FlextTestsTestModels as m,
    )
    from tests.protocols import (
        FlextTestsTestProtocols as FlextTestsTestProtocols,
        FlextTestsTestProtocols as p,
    )
    from tests.test_utils import (
        AssertionHelpers as AssertionHelpers,
        T as T,
        assertion_helpers as assertion_helpers,
    )
    from tests.typings import (
        FlextTestsTestTypes as FlextTestsTestTypes,
        FlextTestsTestTypes as t,
    )
    from tests.unit.flext_tests.test_docker import (
        TestContainerInfo as TestContainerInfo,
        TestContainerStatus as TestContainerStatus,
        TestFlextTestsDocker as TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId as TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot as TestFlextTestsDockerWorkspaceRoot,
    )
    from tests.unit.flext_tests.test_domains import (
        TestFlextTestsDomains as TestFlextTestsDomains,
    )
    from tests.unit.flext_tests.test_files import (
        TestAssertExists as TestAssertExists,
        TestBatchOperations as TestBatchOperations,
        TestCreateInStatic as TestCreateInStatic,
        TestFileInfo as TestFileInfo,
        TestFileInfoFromModels as TestFileInfoFromModels,
        TestFlextTestsFiles as TestFlextTestsFiles,
        TestFlextTestsFilesNewApi as TestFlextTestsFilesNewApi,
        TestInfoWithContentMeta as TestInfoWithContentMeta,
        TestShortAlias as TestShortAlias,
    )
    from tests.unit.flext_tests.test_matchers import (
        TestFlextTestsMatchers as TestFlextTestsMatchers,
    )
    from tests.unit.flext_tests.test_utilities import (
        TestFlextTestsUtilitiesFactory as TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult as TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResultCompat as TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext as TestFlextTestsUtilitiesTestContext,
    )
    from tests.utilities import (
        FlextTestsTestUtilities as FlextTestsTestUtilities,
        FlextTestsTestUtilities as u,
    )

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
    "TestContainerStatus": [
        "tests.unit.flext_tests.test_docker",
        "TestContainerStatus",
    ],
    "TestCreateInStatic": ["tests.unit.flext_tests.test_files", "TestCreateInStatic"],
    "TestFileInfo": ["tests.unit.flext_tests.test_files", "TestFileInfo"],
    "TestFileInfoFromModels": [
        "tests.unit.flext_tests.test_files",
        "TestFileInfoFromModels",
    ],
    "TestFlextTestsDocker": [
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDocker",
    ],
    "TestFlextTestsDockerWorkerId": [
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDockerWorkerId",
    ],
    "TestFlextTestsDockerWorkspaceRoot": [
        "tests.unit.flext_tests.test_docker",
        "TestFlextTestsDockerWorkspaceRoot",
    ],
    "TestFlextTestsDomains": [
        "tests.unit.flext_tests.test_domains",
        "TestFlextTestsDomains",
    ],
    "TestFlextTestsFiles": ["tests.unit.flext_tests.test_files", "TestFlextTestsFiles"],
    "TestFlextTestsFilesNewApi": [
        "tests.unit.flext_tests.test_files",
        "TestFlextTestsFilesNewApi",
    ],
    "TestFlextTestsMatchers": [
        "tests.unit.flext_tests.test_matchers",
        "TestFlextTestsMatchers",
    ],
    "TestFlextTestsUtilitiesFactory": [
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesFactory",
    ],
    "TestFlextTestsUtilitiesResult": [
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesResult",
    ],
    "TestFlextTestsUtilitiesResultCompat": [
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesResultCompat",
    ],
    "TestFlextTestsUtilitiesTestContext": [
        "tests.unit.flext_tests.test_utilities",
        "TestFlextTestsUtilitiesTestContext",
    ],
    "TestInfoWithContentMeta": [
        "tests.unit.flext_tests.test_files",
        "TestInfoWithContentMeta",
    ],
    "TestShortAlias": ["tests.unit.flext_tests.test_files", "TestShortAlias"],
    "assertion_helpers": ["tests.test_utils", "assertion_helpers"],
    "c": ["tests.constants", "FlextTestsTestConstants"],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextTestsTestModels"],
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextTestsTestProtocols"],
    "protocols": ["tests.protocols", ""],
    "r": ["flext_tests", "r"],
    "s": ["flext_tests", "s"],
    "t": ["tests.typings", "FlextTestsTestTypes"],
    "td": ["tests.conftest", "td"],
    "test_utils": ["tests.test_utils", ""],
    "tf": ["tests.conftest", "tf"],
    "tk": ["tests.conftest", "tk"],
    "tm": ["tests.conftest", "tm"],
    "tt": ["tests.conftest", "tt"],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextTestsTestUtilities"],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "td",
    "test_utils",
    "tf",
    "tk",
    "tm",
    "tt",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
