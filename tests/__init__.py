# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.protocols import *
    from tests.test_utils import *
    from tests.typings import *
    from tests.unit.flext_tests import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
