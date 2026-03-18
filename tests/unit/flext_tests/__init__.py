# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit tests for flext_tests namespace.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from .test_builders import TestFlextTestsBuilders
    from .test_docker import (
        TestContainerInfo,
        TestContainerStatus,
        TestFlextTestsDocker,
        TestFlextTestsDockerWorkerId,
        TestFlextTestsDockerWorkspaceRoot,
    )
    from .test_domains import TestFlextTestsDomains
    from .test_factories import (
        TestConfig,
        TestFactoriesHelpers,
        TestFlextTestsFactoriesModernAPI,
        TestService,
        TestService as s,
        TestsFlextTestsFactoriesDict,
        TestsFlextTestsFactoriesGeneric,
        TestsFlextTestsFactoriesList,
        TestsFlextTestsFactoriesModel,
        TestsFlextTestsFactoriesRes,
        TestUser,
    )
    from .test_matchers import TestFlextTestsMatchers
    from .test_utilities import (
        TestFlextTestsUtilitiesFactory,
        TestFlextTestsUtilitiesResult,
        TestFlextTestsUtilitiesResult as r,
        TestFlextTestsUtilitiesResultCompat,
        TestFlextTestsUtilitiesTestContext,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestConfig": ("tests.unit.flext_tests.test_factories", "TestConfig"),
    "TestContainerInfo": ("tests.unit.flext_tests.test_docker", "TestContainerInfo"),
    "TestContainerStatus": (
        "tests.unit.flext_tests.test_docker",
        "TestContainerStatus",
    ),
    "TestFactoriesHelpers": (
        "tests.unit.flext_tests.test_factories",
        "TestFactoriesHelpers",
    ),
    "TestFlextTestsBuilders": (
        "tests.unit.flext_tests.test_builders",
        "TestFlextTestsBuilders",
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
    "TestFlextTestsFactoriesModernAPI": (
        "tests.unit.flext_tests.test_factories",
        "TestFlextTestsFactoriesModernAPI",
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
    "TestService": ("tests.unit.flext_tests.test_factories", "TestService"),
    "TestUser": ("tests.unit.flext_tests.test_factories", "TestUser"),
    "TestsFlextTestsFactoriesDict": (
        "tests.unit.flext_tests.test_factories",
        "TestsFlextTestsFactoriesDict",
    ),
    "TestsFlextTestsFactoriesGeneric": (
        "tests.unit.flext_tests.test_factories",
        "TestsFlextTestsFactoriesGeneric",
    ),
    "TestsFlextTestsFactoriesList": (
        "tests.unit.flext_tests.test_factories",
        "TestsFlextTestsFactoriesList",
    ),
    "TestsFlextTestsFactoriesModel": (
        "tests.unit.flext_tests.test_factories",
        "TestsFlextTestsFactoriesModel",
    ),
    "TestsFlextTestsFactoriesRes": (
        "tests.unit.flext_tests.test_factories",
        "TestsFlextTestsFactoriesRes",
    ),
    "r": ("tests.unit.flext_tests.test_utilities", "TestFlextTestsUtilitiesResult"),
    "s": ("tests.unit.flext_tests.test_factories", "TestService"),
}

__all__ = [
    "TestConfig",
    "TestContainerInfo",
    "TestContainerStatus",
    "TestFactoriesHelpers",
    "TestFlextTestsBuilders",
    "TestFlextTestsDocker",
    "TestFlextTestsDockerWorkerId",
    "TestFlextTestsDockerWorkspaceRoot",
    "TestFlextTestsDomains",
    "TestFlextTestsFactoriesModernAPI",
    "TestFlextTestsMatchers",
    "TestFlextTestsUtilitiesFactory",
    "TestFlextTestsUtilitiesResult",
    "TestFlextTestsUtilitiesResultCompat",
    "TestFlextTestsUtilitiesTestContext",
    "TestService",
    "TestUser",
    "TestsFlextTestsFactoriesDict",
    "TestsFlextTestsFactoriesGeneric",
    "TestsFlextTestsFactoriesList",
    "TestsFlextTestsFactoriesModel",
    "TestsFlextTestsFactoriesRes",
    "r",
    "s",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
