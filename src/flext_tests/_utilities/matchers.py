"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._matchers._assertions import FlextTestsMatchersAssertionsMixin
from ._matchers._containment import FlextTestsMatchersContainmentMixin
from ._matchers._immutability import FlextTestsMatchersImmutabilityMixin
from ._matchers._result import FlextTestsMatchersResultMixin
from ._matchers._scope import FlextTestsMatchersScopeMixin
from ._matchers._that import FlextTestsMatchersThatMixin
from ._matchers._typeguards import FlextTestsMatchersTypeGuardsMixin


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


tm = FlextTestsMatchersUtilities.Tests.Matchers
__all__: list[str] = ["FlextTestsMatchersUtilities", "tm"]
