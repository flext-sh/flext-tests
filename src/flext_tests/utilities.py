"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_tests._utilities import (
    FlextTestsEnforcementUtilitiesMixin,
    FlextTestsEnvironmentUtilitiesMixin,
    FlextTestsFlextUtilitiesGovernance,
    FlextTestsFlextUtilitiesHandler,
    FlextTestsFlextUtilitiesMakeContract,
    FlextTestsFlextUtilitiesPayload,
    FlextTestsMakeParsingUtilitiesMixin,
    FlextTestsMakeRegistryUtilitiesMixin,
    FlextTestsMakeRenderingUtilitiesMixin,
    FlextTestsMakeUtilitiesMixin,
    FlextTestsMatchersUtilities,
    FlextTestsNamespaceUtilitiesMixin,
    FlextTestsScratchStorageUtilitiesMixin,
    FlextTestsUtilitiesBase,
    FlextTestsWorkspaceCleanupGitUtilitiesMixin,
    FlextTestsWorkspaceCleanupInspectUtilitiesMixin,
    FlextTestsWorkspaceCleanupPathsUtilitiesMixin,
    FlextTestsWorkspaceCleanupPlanUtilitiesMixin,
    FlextTestsWorkspaceCleanupUtilitiesMixin,
)
from flext_tests._utilities.container import FlextTestsContainerHelpersUtilitiesMixin
from flext_tests._utilities.docker_lifecycle import (
    FlextTestsDockerLifecycleUtilitiesMixin,
)
from flext_tests._utilities.docker_state import FlextTestsDockerStateUtilitiesMixin
from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
from flext_tests._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin


class FlextTestsUtilities(FlextCliUtilities, FlextTestsFlextUtilitiesGovernance):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        FlextTestsUtilitiesBase,
        FlextTestsEnforcementUtilitiesMixin,
        FlextTestsEnvironmentUtilitiesMixin,
        FlextTestsFlextUtilitiesGovernance,
        FlextTestsFlextUtilitiesHandler,
        FlextTestsMakeUtilitiesMixin,
        FlextTestsMakeRenderingUtilitiesMixin,
        FlextTestsMakeRegistryUtilitiesMixin,
        FlextTestsMakeParsingUtilitiesMixin,
        FlextTestsFlextUtilitiesMakeContract,
        FlextTestsMatchersUtilities,
        FlextTestsNamespaceUtilitiesMixin,
        FlextTestsFlextUtilitiesPayload,
        FlextTestsScratchStorageUtilitiesMixin,
        FlextTestsWorkspaceCleanupUtilitiesMixin,
        FlextTestsWorkspaceCleanupPlanUtilitiesMixin,
        FlextTestsWorkspaceCleanupInspectUtilitiesMixin,
        FlextTestsWorkspaceCleanupPathsUtilitiesMixin,
        FlextTestsWorkspaceCleanupGitUtilitiesMixin,
        FlextTestsResultUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsDockerStateUtilitiesMixin,
        FlextTestsDockerLifecycleUtilitiesMixin,
        FlextTestsGenericHelpersUtilitiesMixin,
        FlextTestsConfigHelpersUtilitiesMixin,
        FlextTestsContainerHelpersUtilitiesMixin,
        FlextTestsFlextUtilitiesHandler.FlextTestsHandlerHelpersUtilitiesMixin,
        FlextTestsFilesUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
        FlextTestsFixturesDSLMixin,
        FlextTestsFlextUtilitiesGovernance.FlextTestsModuleGovernanceMixin,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities

__all__: list[str] = [
    "FlextTestsFixturesDSLMixin",
    "FlextTestsUtilities",
    "u",
]
