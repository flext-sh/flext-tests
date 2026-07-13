"""Constants for flext-tests tests.

Provides TestsFlextTestsConstants, extending FlextTestsConstants with
flext-tests-specific constants. All generic test constants come from flext_tests.

Architecture:
- FlextTestsConstants (flext_tests) = Generic constants for all FLEXT projects
- TestsFlextTestsConstants (tests/) = flext-tests-specific constants extending FlextTestsConstants

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants


class TestsFlextTestsConstants(FlextTestsConstants):
    """Test constants for flext-tests - extends FlextTestsConstants.

    Architecture: Extends FlextTestsConstants with flext-tests-specific constants.
    All generic constants from FlextTestsConstants are available through inheritance.

    Rules:
    - NEVER duplicate constants from FlextTestsConstants
    - Only flext-tests-specific constants allowed
    - All generic constants come from FlextTestsConstants
    """

    class Tests(FlextTestsConstants.Tests):
        """flext-tests test constants namespace."""


c = TestsFlextTestsConstants

__all__: list[str] = ["TestsFlextTestsConstants", "c"]
