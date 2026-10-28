# AUTO-GENERATED FILE — Regenerate with: make gen
"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u as flext_cli_u

from flext_tests._utilities import (
    FlextTestsUtilitiesBase,
    FlextTestsUtilitiesConfigHelpers,
    FlextTestsUtilitiesContainerHelpers,
    FlextTestsUtilitiesDockerClient,
    FlextTestsUtilitiesDockerLifecycle,
    FlextTestsUtilitiesDockerState,
    FlextTestsUtilitiesEnforcement,
    FlextTestsUtilitiesEnvironment,
    FlextTestsUtilitiesFiles,
    FlextTestsUtilitiesFixturesDSL,
    FlextTestsUtilitiesFlextGovernance,
    FlextTestsUtilitiesFlextHandler,
    FlextTestsUtilitiesNamespace,
    FlextTestsUtilitiesPayload,
    FlextTestsUtilitiesPytest,
    FlextTestsUtilitiesResult,
    FlextTestsUtilitiesScratchStorage,
    FlextTestsUtilitiesTestContext,
)


class FlextTestsUtilities(flext_cli_u, FlextTestsUtilitiesFlextGovernance):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        FlextTestsUtilitiesContainerHelpers,
        FlextTestsUtilitiesDockerClient,
        FlextTestsUtilitiesDockerLifecycle,
        FlextTestsUtilitiesDockerState,
        FlextTestsUtilitiesEnforcement,
        FlextTestsUtilitiesEnvironment,
        FlextTestsUtilitiesFiles,
        FlextTestsUtilitiesFixturesDSL,
        FlextTestsUtilitiesNamespace,
        FlextTestsUtilitiesPayload,
        FlextTestsUtilitiesResult,
        FlextTestsUtilitiesScratchStorage,
        FlextTestsUtilitiesConfigHelpers,
        FlextTestsUtilitiesTestContext,
        FlextTestsUtilitiesBase,
        FlextTestsUtilitiesPytest,
        FlextTestsUtilitiesFlextHandler.FlextTestsUtilitiesHandlerHelpers,
        FlextTestsUtilitiesFlextGovernance.FlextTestsModuleGovernance,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities
__all__: list[str] = ["FlextTestsUtilities", "FlextTestsUtilitiesFixturesDSL", "u"]
