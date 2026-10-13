"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests._utilities._matchers import (
    FlextTestsMatchersAssertionsMixin,
    FlextTestsMatchersContainmentMixin,
    FlextTestsMatchersImmutabilityMixin,
    FlextTestsMatchersResultMixin,
    FlextTestsMatchersScopeMixin,
    FlextTestsMatchersThatMixin,
    FlextTestsMatchersTypeGuardsMixin,
)


class FlextTestsMatchersUtilities:
    """Namespace for test matcher utilities used in flext-tests."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(
            FlextTestsMatchersContainmentMixin,
            FlextTestsMatchersImmutabilityMixin.Tests.Matchers,
            FlextTestsMatchersResultMixin.Tests.Matchers,
            FlextTestsMatchersScopeMixin.Tests.Matchers,
            FlextTestsMatchersThatMixin.Tests.Matchers,
            FlextTestsMatchersTypeGuardsMixin,
            FlextTestsMatchersAssertionsMixin,
        ):
            """Test matchers with powerful generalist methods."""


__all__: list[str] = ["FlextTestsMatchersUtilities"]
