"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests._utilities import (
    FlextTestsUtilitiesMatchersAssertions,
    FlextTestsUtilitiesMatchersContainment,
    FlextTestsUtilitiesMatchersImmutability,
    FlextTestsUtilitiesMatchersResult,
    FlextTestsUtilitiesMatchersScope,
    FlextTestsUtilitiesMatchersThat,
    FlextTestsUtilitiesMatchersTypeguards,
)


class FlextTestsMatchersUtilities:
    """Namespace for test matcher utilities used in flext-tests."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(
            FlextTestsUtilitiesMatchersContainment,
            FlextTestsUtilitiesMatchersImmutability.Tests.Matchers,
            FlextTestsUtilitiesMatchersResult.Tests.Matchers,
            FlextTestsUtilitiesMatchersScope.Tests.Matchers,
            FlextTestsUtilitiesMatchersThat.Tests.Matchers,
            FlextTestsUtilitiesMatchersTypeguards,
            FlextTestsUtilitiesMatchersAssertions,
        ):
            """Test matchers with powerful generalist methods."""


__all__: list[str] = ["FlextTestsMatchersUtilities"]
