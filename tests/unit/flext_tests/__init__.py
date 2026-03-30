# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from tests.unit.flext_tests.test_docker import *
    from tests.unit.flext_tests.test_domains import *
    from tests.unit.flext_tests.test_files import *
    from tests.unit.flext_tests.test_matchers import *
    from tests.unit.flext_tests.test_utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
    "test_docker": "tests.unit.flext_tests.test_docker",
    "test_domains": "tests.unit.flext_tests.test_domains",
    "test_files": "tests.unit.flext_tests.test_files",
    "test_matchers": "tests.unit.flext_tests.test_matchers",
    "test_utilities": "tests.unit.flext_tests.test_utilities",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
