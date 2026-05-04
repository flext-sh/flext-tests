"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import u
from flext_tests import (
    FlextTestsConfigHelpersUtilitiesMixin,
    FlextTestsContainerHelpersUtilitiesMixin,
    FlextTestsFilesUtilitiesMixin,
    FlextTestsGenericHelpersUtilitiesMixin,
    FlextTestsHandlerHelpersUtilitiesMixin,
    FlextTestsMatchersUtilities,
    FlextTestsResultUtilitiesMixin,
    FlextTestsTestContextUtilitiesMixin,
    FlextTestsValidatorUtilitiesMixin,
)


class FlextTestsUtilities(u):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        FlextTestsResultUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsGenericHelpersUtilitiesMixin,
        FlextTestsConfigHelpersUtilitiesMixin,
        FlextTestsContainerHelpersUtilitiesMixin,
        FlextTestsHandlerHelpersUtilitiesMixin,
        FlextTestsFilesUtilitiesMixin,
        FlextTestsValidatorUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities

__all__: list[str] = ["FlextTestsUtilities", "u"]
