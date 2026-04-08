"""Type system foundation for flext-tests tests.

Provides TestsFlextTestsTypes, extending TestsFlextTypes with
flext-tests-specific type definitions.

Architecture:
- TestsFlextTypes (flext_tests) = Generic types for all FLEXT projects
- TestsFlextTestsTypes (tests/) = flext-tests-specific types extending TestsFlextTypes

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes


class TestsFlextTestsTypes(FlextTestsTypes):
    """Type system foundation for flext-tests tests - extends TestsFlextTypes.

    Architecture: Extends TestsFlextTypes with flext-tests-specific type definitions.
    All generic types from TestsFlextTypes are available through inheritance.

    Rules:
    - NEVER redeclare types from TestsFlextTypes
    - Only flext-tests-specific types allowed
    - All generic types come from TestsFlextTypes
    """

    class Tests(FlextTestsTypes.Tests):
        """flext-tests-specific type definitions namespace."""


t = TestsFlextTestsTypes

__all__ = ["TestsFlextTestsTypes", "t"]
