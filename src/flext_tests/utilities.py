"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending FlextCliUtilities with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli.utilities import FlextCliUtilities
from flext_tests import (
    FlextTestsAssertionsUtilitiesMixin,
    FlextTestsBadObjectsUtilitiesMixin,
    FlextTestsConfigHelpersUtilitiesMixin,
    FlextTestsConstantsHelpersUtilitiesMixin,
    FlextTestsContainerHelpersUtilitiesMixin,
    FlextTestsContextHelpersUtilitiesMixin,
    FlextTestsDomainHelpersUtilitiesMixin,
    FlextTestsExceptionHelpersUtilitiesMixin,
    FlextTestsFilesUtilitiesMixin,
    FlextTestsGenericHelpersUtilitiesMixin,
    FlextTestsHandlerHelpersUtilitiesMixin,
    FlextTestsMatchersUtilities,
    FlextTestsParserHelpersUtilitiesMixin,
    FlextTestsResultUtilitiesMixin,
    FlextTestsTestCaseHelpersUtilitiesMixin,
    FlextTestsTestContextUtilitiesMixin,
    FlextTestsValidationUtilitiesMixin,
    FlextTestsValidatorUtilitiesMixin,
)


class FlextTestsUtilities(FlextCliUtilities):
    """Test utilities for FLEXT ecosystem - extends FlextCliUtilities.

    Provides essential test helpers that complement FlextCliUtilities.
    All FlextCliUtilities functionality is available via inheritance.
    """

    class Tests(
        FlextTestsValidationUtilitiesMixin,
        FlextTestsResultUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsGenericHelpersUtilitiesMixin,
        FlextTestsConfigHelpersUtilitiesMixin,
        FlextTestsContextHelpersUtilitiesMixin,
        FlextTestsContainerHelpersUtilitiesMixin,
        FlextTestsHandlerHelpersUtilitiesMixin,
        FlextTestsParserHelpersUtilitiesMixin,
        FlextTestsTestCaseHelpersUtilitiesMixin,
        FlextTestsDomainHelpersUtilitiesMixin,
        FlextTestsExceptionHelpersUtilitiesMixin,
        FlextTestsBadObjectsUtilitiesMixin,
        FlextTestsConstantsHelpersUtilitiesMixin,
        FlextTestsAssertionsUtilitiesMixin,
        FlextTestsFilesUtilitiesMixin,
        FlextTestsValidatorUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities

__all__: list[str] = ["FlextTestsUtilities", "u"]
