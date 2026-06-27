"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import (
    FlextTestsMatchersAssertionsMixin,
    FlextTestsMatchersContainmentMixin,
    FlextTestsMatchersResultMixin,
    FlextTestsMatchersScopeMixin,
    FlextTestsMatchersThatMixin,
    FlextTestsMatchersTypeGuardsMixin,
)


class FlextTestsMatchersUtilities(
    FlextTestsMatchersContainmentMixin,
    FlextTestsMatchersResultMixin,
    FlextTestsMatchersScopeMixin,
    FlextTestsMatchersThatMixin,
    FlextTestsMatchersTypeGuardsMixin,
    FlextTestsMatchersAssertionsMixin,
):
    """Namespace for test matcher utilities used in flext-tests."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(
            FlextTestsMatchersResultMixin.Tests.Matchers,
            FlextTestsMatchersScopeMixin.Tests.Matchers,
            FlextTestsMatchersThatMixin.Tests.Matchers,
        ):
            """Test matchers with powerful generalist methods."""


tm = FlextTestsMatchersUtilities.Tests.Matchers
__all__: list[str] = ["FlextTestsMatchersUtilities", "tm"]
