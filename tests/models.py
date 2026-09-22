"""Models for flext-tests tests.

Provides TestsFlextTestsModels, extending TestsFlextModels with
flext-tests-specific model definitions.

Architecture:
- TestsFlextModels (flext_tests) = Generic models for all FLEXT projects
- TestsFlextTestsModels (tests/) = flext-tests-specific models extending TestsFlextModels

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels


class TestsFlextTestsModels(FlextTestsModels):
    """Test models for flext-tests - extends TestsFlextModels.

    Architecture: Extends TestsFlextModels with flext-tests-specific model definitions.
    All base models from TestsFlextModels are available through inheritance.
    """

    class Tests(FlextTestsModels.Tests):
        """flext-tests test models namespace."""


m = TestsFlextTestsModels

__all__: list[str] = ["TestsFlextTestsModels", "m"]
