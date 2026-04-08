"""Utilities for flext-tests tests.

Provides TestsFlextTestsUtilities, extending TestsFlextUtilities with
flext-tests-specific utilities.

Architecture:
- TestsFlextUtilities (flext_tests) = Generic utilities for all FLEXT projects
- TestsFlextTestsUtilities (tests/) = flext-tests-specific utilities extending TestsFlextUtilities

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities


class TestsFlextTestsUtilities(FlextTestsUtilities):
    """Utilities for flext-tests tests - extends TestsFlextUtilities.

    Architecture: Extends TestsFlextUtilities with flext-tests-specific utility
    definitions. All generic utilities from TestsFlextUtilities are available
    through inheritance.

    Rules:
    - NEVER redeclare utilities from TestsFlextUtilities
    - Only flext-tests-specific utilities allowed
    - All generic utilities come from TestsFlextUtilities
    """

    class Tests(FlextTestsUtilities.Tests):
        """flext-tests-specific test utilities namespace."""


u = TestsFlextTestsUtilities

__all__ = ["TestsFlextTestsUtilities", "u"]
