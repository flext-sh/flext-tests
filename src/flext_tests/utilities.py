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
    FlextTestsUtilitiesMatchers,
    FlextTestsUtilitiesNamespace,
    FlextTestsUtilitiesPayload,
    FlextTestsUtilitiesPytest,
    FlextTestsUtilitiesResult,
    FlextTestsUtilitiesScratchStorage,
    FlextTestsUtilitiesTestContext,
)


class FlextTestsUtilities(
    flext_cli_u,
    FlextTestsUtilitiesFlextGovernance,
    # Assertion matchers (that/...) published at the u root: test modules
    # call `u.that(...)` / `tm.that(...)` directly (strict no-subnamespace).
    FlextTestsUtilitiesMatchers,
):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        # Assertion matchers publish `that` and siblings into the Tests
        # namespace (ldap family precedent: Tests.that(subject, ...)).
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
        FlextTestsUtilitiesMatchers,
        FlextTestsUtilitiesNamespace,
        FlextTestsUtilitiesPayload,
        FlextTestsUtilitiesPytest,
        FlextTestsUtilitiesResult,
        FlextTestsUtilitiesScratchStorage,
        FlextTestsUtilitiesConfigHelpers,
        FlextTestsUtilitiesTestContext,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities
__all__: list[str] = ["FlextTestsUtilities", "FlextTestsUtilitiesFixturesDSL", "u"]
