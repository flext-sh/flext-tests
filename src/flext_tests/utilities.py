"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import u

from ._utilities.container import FlextTestsContainerHelpersUtilitiesMixin
from ._utilities.files import FlextTestsFilesUtilitiesMixin
from ._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
from ._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
from ._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin
from ._utilities.make import FlextTestsMakeUtilitiesMixin
from ._utilities.matchers import FlextTestsMatchersUtilities
from ._utilities.result import FlextTestsResultUtilitiesMixin
from ._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
from ._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
from ._utilities.validator import FlextTestsValidatorUtilitiesMixin
from ._utilities.workspace_cleanup import FlextTestsWorkspaceCleanupUtilitiesMixin


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
        FlextTestsMakeUtilitiesMixin,
        FlextTestsValidatorUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
        FlextTestsFixturesDSLMixin,
        # NOTE (multi-agent): compose guarded cleanup planning/apply into u.Tests.
        FlextTestsWorkspaceCleanupUtilitiesMixin,
    ):
        """Test utilities namespace."""


u = FlextTestsUtilities

__all__: list[str] = ["FlextTestsFixturesDSLMixin", "FlextTestsUtilities", "u"]
