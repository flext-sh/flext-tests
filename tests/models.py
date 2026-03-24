"""Models for flext-tests tests.

Provides FlextTestsTestModels, extending FlextTestsModels with
flext-tests-specific model definitions.

Architecture:
- FlextTestsModels (flext_tests) = Generic models for all FLEXT projects
- FlextTestsTestModels (tests/) = flext-tests-specific models extending FlextTestsModels

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels


class FlextTestsTestModels(FlextTestsModels):
    """Test models for flext-tests - extends FlextTestsModels.

    Architecture: Extends FlextTestsModels with flext-tests-specific model definitions.
    All base models from FlextTestsModels are available through inheritance.
    """

    class Tests(FlextTestsModels.Tests):
        """flext-tests-specific test models namespace."""


m = FlextTestsTestModels

__all__ = ["FlextTestsTestModels", "m"]
