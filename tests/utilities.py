"""Utilities for flext-tests tests.

Provides FlextTestsTestUtilities, extending FlextTestsUtilities with
flext-tests-specific utilities.

Architecture:
- FlextTestsUtilities (flext_tests) = Generic utilities for all FLEXT projects
- FlextTestsTestUtilities (tests/) = flext-tests-specific utilities extending FlextTestsUtilities

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities


class FlextTestsTestUtilities(FlextTestsUtilities):
    """Utilities for flext-tests tests - extends FlextTestsUtilities.

    Architecture: Extends FlextTestsUtilities with flext-tests-specific utility
    definitions. All generic utilities from FlextTestsUtilities are available
    through inheritance.

    Rules:
    - NEVER redeclare utilities from FlextTestsUtilities
    - Only flext-tests-specific utilities allowed
    - All generic utilities come from FlextTestsUtilities
    """

    class Tests(FlextTestsUtilities.Tests):
        """flext-tests-specific test utilities namespace."""


u = FlextTestsTestUtilities

__all__ = ["FlextTestsTestUtilities", "u"]
