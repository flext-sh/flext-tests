"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending FlextCliUtilities with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u as _cli_u
from flext_tests._utilities.assertions import FlextTestsAssertionsUtilitiesMixin
from flext_tests._utilities.badobjects import FlextTestsBadObjectsUtilitiesMixin
from flext_tests._utilities.config import FlextTestsConfigHelpersUtilitiesMixin
from flext_tests._utilities.constants import FlextTestsConstantsHelpersUtilitiesMixin
from flext_tests._utilities.container import FlextTestsContainerHelpersUtilitiesMixin
from flext_tests._utilities.context import FlextTestsContextHelpersUtilitiesMixin
from flext_tests._utilities.deepmatch import FlextTestsDeepMatchUtilitiesMixin
from flext_tests._utilities.domain import FlextTestsDomainHelpersUtilitiesMixin
from flext_tests._utilities.exception import FlextTestsExceptionHelpersUtilitiesMixin
from flext_tests._utilities.factory import FlextTestsFactoryUtilitiesMixin
from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
from flext_tests._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin
from flext_tests._utilities.length import FlextTestsLengthUtilitiesMixin
from flext_tests._utilities.matchers import FlextTestsMatchersUtilities
from flext_tests._utilities.parser import FlextTestsParserHelpersUtilitiesMixin
from flext_tests._utilities.registry import FlextTestsRegistryHelpersUtilitiesMixin
from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
from flext_tests._utilities.testcase import FlextTestsTestCaseHelpersUtilitiesMixin
from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
from flext_tests._utilities.validation import FlextTestsValidationUtilitiesMixin
from flext_tests._utilities.validator import FlextTestsValidatorUtilitiesMixin


class FlextTestsUtilities(_cli_u):
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
