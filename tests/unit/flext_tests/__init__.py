# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit.flext_tests import (
        test_docker as test_docker,
        test_domains as test_domains,
        test_files as test_files,
        test_matchers as test_matchers,
        test_utilities as test_utilities,
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

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
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
    "test_docker": ["tests.unit.flext_tests.test_docker", ""],
    "test_domains": ["tests.unit.flext_tests.test_domains", ""],
    "test_files": ["tests.unit.flext_tests.test_files", ""],
    "test_matchers": ["tests.unit.flext_tests.test_matchers", ""],
    "test_utilities": ["tests.unit.flext_tests.test_utilities", ""],
}

_EXPORTS: Sequence[str] = [
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
    "test_docker",
    "test_domains",
    "test_files",
    "test_matchers",
    "test_utilities",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
