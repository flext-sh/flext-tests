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
    FlextTestsUtilitiesMatchers,
    FlextTestsUtilitiesNamespace,
    FlextTestsUtilitiesPayload,
    FlextTestsUtilitiesPytest,
    FlextTestsUtilitiesResult,
    FlextTestsUtilitiesScratchStorage,
    FlextTestsUtilitiesTestContext,
)
from flext_tests._utilities.governance import FlextTestsUtilitiesFlextGovernance
from flext_tests._utilities.handler import FlextTestsUtilitiesFlextHandler


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
        FlextTestsUtilitiesNamespace,
        FlextTestsUtilitiesPayload,
        FlextTestsUtilitiesResult,
        FlextTestsUtilitiesScratchStorage,
        FlextTestsUtilitiesConfigHelpers,
        FlextTestsUtilitiesTestContext,
        FlextTestsUtilitiesBase,
        FlextTestsUtilitiesPytest,
        FlextTestsUtilitiesMatchers,
        FlextTestsUtilitiesFlextHandler,
        FlextTestsUtilitiesFlextGovernance,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities
__all__: list[str] = ["FlextTestsUtilities", "FlextTestsUtilitiesFixturesDSL", "u"]
