# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

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

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.test_utils as _tests_test_utils

    test_utils = _tests_test_utils
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        AssertionHelpers,
        FlextTestsTestConstants,
        FlextTestsTestModels,
        FlextTestsTestProtocols,
        FlextTestsTestTypes,
        FlextTestsTestUtilities,
        T,
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
        assertion_helpers,
        c,
        conftest,
        constants,
        d,
        e,
        h,
        m,
        models,
        p,
        protocols,
        r,
        s,
        t,
        td,
        test_utils,
        tf,
        tk,
        tm,
        tt,
        typings,
        u,
        utilities,
        x,
    )
_LAZY_IMPORTS = {
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
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTestsTestModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTestsTestProtocols"),
    "protocols": "tests.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
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
    "x": ("flext_core.mixins", "FlextMixins"),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
