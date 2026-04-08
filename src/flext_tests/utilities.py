"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending FlextCliUtilities with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u
from flext_tests import (
    FlextTestsAssertionsUtilitiesMixin,
    FlextTestsBadObjectsUtilitiesMixin,
    FlextTestsConfigHelpersUtilitiesMixin,
    FlextTestsConstantsHelpersUtilitiesMixin,
    FlextTestsContainerHelpersUtilitiesMixin,
    FlextTestsContextHelpersUtilitiesMixin,
    FlextTestsDeepMatchUtilitiesMixin,
    FlextTestsDomainHelpersUtilitiesMixin,
    FlextTestsExceptionHelpersUtilitiesMixin,
    FlextTestsFactoryUtilitiesMixin,
    FlextTestsFilesUtilitiesMixin,
    FlextTestsGenericHelpersUtilitiesMixin,
    FlextTestsHandlerHelpersUtilitiesMixin,
    FlextTestsLengthUtilitiesMixin,
    FlextTestsMatchersUtilities,
    FlextTestsParserHelpersUtilitiesMixin,
    FlextTestsRegistryHelpersUtilitiesMixin,
    FlextTestsResultUtilitiesMixin,
    FlextTestsTestCaseHelpersUtilitiesMixin,
    FlextTestsTestContextUtilitiesMixin,
    FlextTestsValidationUtilitiesMixin,
    FlextTestsValidatorUtilitiesMixin,
)


class FlextTestsUtilities(u):
    """Test utilities for FLEXT ecosystem - extends FlextCliUtilities.

    Provides essential test helpers that complement FlextCliUtilities.
    All FlextCliUtilities functionality is available via inheritance.
    """

    class Tests(
        FlextTestsValidationUtilitiesMixin,
        FlextTestsResultUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsFactoryUtilitiesMixin,
        FlextTestsGenericHelpersUtilitiesMixin,
        FlextTestsRegistryHelpersUtilitiesMixin,
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
        FlextTestsDeepMatchUtilitiesMixin,
        FlextTestsLengthUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
    ):
        """Test utilities namespace."""

        class Factory(FlextTestsFactoryUtilitiesMixin):
            """Factory namespace for test data creation."""


u = FlextTestsUtilities

__all__ = ["FlextTestsUtilities", "u"]
