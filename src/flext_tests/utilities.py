# AUTO-GENERATED FILE — Regenerate with: make gen
"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_tests._utilities import (
    FlextTestsConfigHelpersUtilitiesMixin,
    FlextTestsContainerHelpersUtilitiesMixin,
    FlextTestsDockerClientUtilitiesMixin,
    FlextTestsDockerLifecycleUtilitiesMixin,
    FlextTestsDockerStateUtilitiesMixin,
    FlextTestsEnforcementUtilitiesMixin,
    FlextTestsEnvironmentUtilitiesMixin,
    FlextTestsFilesUtilitiesMixin,
    FlextTestsFixturesDSLMixin,
    FlextTestsFlextUtilitiesGovernance,
    FlextTestsFlextUtilitiesHandler,
    FlextTestsFlextUtilitiesPayload,
    FlextTestsMatchersUtilities,
    FlextTestsNamespaceUtilitiesMixin,
    FlextTestsResultUtilitiesMixin,
    FlextTestsScratchStorageUtilitiesMixin,
    FlextTestsTestContextUtilitiesMixin,
    FlextTestsUtilitiesBase,
)


class FlextTestsUtilities(FlextCliUtilities, FlextTestsFlextUtilitiesGovernance):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        FlextTestsUtilitiesBase,
        FlextTestsContainerHelpersUtilitiesMixin,
        FlextTestsDockerClientUtilitiesMixin,
        FlextTestsDockerLifecycleUtilitiesMixin,
        FlextTestsDockerStateUtilitiesMixin,
        FlextTestsEnforcementUtilitiesMixin,
        FlextTestsEnvironmentUtilitiesMixin,
        FlextTestsFilesUtilitiesMixin,
        FlextTestsFixturesDSLMixin,
        FlextTestsNamespaceUtilitiesMixin,
        FlextTestsFlextUtilitiesPayload,
        FlextTestsResultUtilitiesMixin,
        FlextTestsScratchStorageUtilitiesMixin,
        FlextTestsConfigHelpersUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsFlextUtilitiesHandler.FlextTestsHandlerHelpersUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
        FlextTestsFlextUtilitiesGovernance.FlextTestsModuleGovernanceMixin,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities

__all__: list[str] = [
    "FlextTestsFixturesDSLMixin",
    "FlextTestsUtilities",
    "u",
]
