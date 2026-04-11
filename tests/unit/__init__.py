# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_tests.test_docker import (
        TestContainerInfo,
        TestContainerStatus,
        TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot,
    )
    from flext_tests.test_domains import TestFlextTestsDomains
    from flext_tests.test_files import (
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
    from flext_tests.test_matchers import TestFlextTestsMatchers
    from flext_tests.test_utilities import (
        TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_docker": (
            "TestContainerInfo",
            "TestContainerStatus",
            "TestFlextTestsDocker",
            "TestFlextTestsDockerWorkerId",
            "TestFlextTestsDockerWorkspaceRoot",
        ),
        ".test_domains": ("TestFlextTestsDomains",),
        ".test_files": (
            "TestAssertExists",
            "TestBatchOperations",
            "TestCreateInStatic",
            "TestFileInfo",
            "TestFileInfoFromModels",
            "TestFlextTestsFiles",
            "TestFlextTestsFilesNewApi",
            "TestInfoWithContentMeta",
            "TestShortAlias",
        ),
        ".test_matchers": ("TestFlextTestsMatchers",),
        ".test_utilities": (
            "TestFlextTestsUtilitiesFactory",
            "TestFlextTestsUtilitiesResult",
            "TestFlextTestsUtilitiesResultCompat",
            "TestFlextTestsUtilitiesTestContext",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
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
]
