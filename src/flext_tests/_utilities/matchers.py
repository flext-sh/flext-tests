"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests._utilities._matchers import (
    FlextTestsUtilitiesMatchersAssertions,
    FlextTestsUtilitiesMatchersContainment,
    FlextTestsUtilitiesMatchersImmutability,
    FlextTestsUtilitiesMatchersResult,
    FlextTestsUtilitiesMatchersScope,
    FlextTestsUtilitiesMatchersThat,
    FlextTestsUtilitiesMatchersTypeguards,
)


class FlextTestsUtilitiesMatchers(
    FlextTestsUtilitiesMatchersAssertions,
    FlextTestsUtilitiesMatchersContainment,
    FlextTestsUtilitiesMatchersImmutability,
    FlextTestsUtilitiesMatchersResult,
    FlextTestsUtilitiesMatchersScope,
    FlextTestsUtilitiesMatchersThat,
    FlextTestsUtilitiesMatchersTypeguards,
):
    """Namespace for test matcher utilities used in flext-tests."""


__all__: list[str] = ["FlextTestsUtilitiesMatchers"]
