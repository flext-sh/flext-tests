"""Type system foundation for flext-tests tests.

Provides FlextTestsTestTypes, extending FlextTestsTypes with
flext-tests-specific type definitions.

Architecture:
- FlextTestsTypes (flext_tests) = Generic types for all FLEXT projects
- FlextTestsTestTypes (tests/) = flext-tests-specific types extending FlextTestsTypes

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes


class FlextTestsTestTypes(FlextTestsTypes):
    """Type system foundation for flext-tests tests - extends FlextTestsTypes.

    Architecture: Extends FlextTestsTypes with flext-tests-specific type definitions.
    All generic types from FlextTestsTypes are available through inheritance.

    Rules:
    - NEVER redeclare types from FlextTestsTypes
    - Only flext-tests-specific types allowed
    - All generic types come from FlextTestsTypes
    """

    class Tests(FlextTestsTypes.Tests):
        """flext-tests-specific type definitions namespace."""


t = FlextTestsTestTypes

__all__ = ["FlextTestsTestTypes", "t"]
