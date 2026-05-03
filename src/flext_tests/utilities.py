"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending FlextCliUtilities with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities
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


class FlextTestsUtilities(FlextCliUtilities):
    """Test utilities for FLEXT ecosystem - extends FlextCliUtilities.

    Provides essential test helpers that complement FlextCliUtilities.
    All FlextCliUtilities functionality is available via inheritance.
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
