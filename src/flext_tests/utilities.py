"""Test utilities for FLEXT ecosystem tests.

Provides essential test utilities extending u with test-specific
helpers for result validation, context management, and test data creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_cli import FlextCliUtilities

from flext_tests._utilities.container import FlextTestsContainerHelpersUtilitiesMixin
from flext_tests._utilities.docker_lifecycle import (
    FlextTestsDockerLifecycleUtilitiesMixin,
)
from flext_tests._utilities.docker_state import FlextTestsDockerStateUtilitiesMixin
from flext_tests._utilities.enforcement import FlextTestsEnforcementUtilitiesMixin
from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
from flext_tests._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
from flext_tests._utilities.governance import FlextTestsFlextUtilitiesGovernance
from flext_tests._utilities.handler import FlextTestsFlextUtilitiesHandler
from flext_tests._utilities.make import FlextTestsMakeUtilitiesMixin
from flext_tests._utilities.matchers import FlextTestsMatchersUtilities
from flext_tests._utilities.namespace import FlextTestsNamespaceUtilitiesMixin
from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
from flext_tests._utilities.scratch_storage import (
    FlextTestsScratchStorageUtilitiesMixin,
)
from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
from flext_tests._utilities.workspace_cleanup import (
    FlextTestsWorkspaceCleanupUtilitiesMixin,
)


class FlextTestsUtilities(FlextCliUtilities, FlextTestsFlextUtilitiesGovernance):
    """Test utilities for FLEXT ecosystem - extends u.

    Provides essential test helpers that complement u.
    All u functionality is available via inheritance.
    """

    class Tests(
        FlextTestsResultUtilitiesMixin,
        FlextTestsTestContextUtilitiesMixin,
        FlextTestsDockerStateUtilitiesMixin,
        FlextTestsScratchStorageUtilitiesMixin,
        FlextTestsDockerLifecycleUtilitiesMixin,
        FlextTestsGenericHelpersUtilitiesMixin,
        FlextTestsConfigHelpersUtilitiesMixin,
        FlextTestsContainerHelpersUtilitiesMixin,
        FlextTestsFlextUtilitiesHandler.FlextTestsHandlerHelpersUtilitiesMixin,
        FlextTestsFilesUtilitiesMixin,
        FlextTestsMakeUtilitiesMixin,
        FlextTestsMatchersUtilities.Tests,
        FlextTestsFixturesDSLMixin,
        # NOTE (multi-agent): compose guarded cleanup planning/apply into u.Tests.
        FlextTestsWorkspaceCleanupUtilitiesMixin,
        FlextTestsFlextUtilitiesGovernance.FlextTestsModuleGovernanceMixin,
        FlextTestsEnforcementUtilitiesMixin,
        FlextTestsNamespaceUtilitiesMixin,
    ):
        """Test utilities namespace."""

        # Single consumer surface for the options model of create_handler_config:
        # callers reach it as u.Tests.FlextTestsHandlerConfigParams. ClassVar
        # keeps the class object out of any pydantic field synthesis in the
        # composed namespace.
        FlextTestsHandlerConfigParams: ClassVar[
            type[FlextTestsFlextUtilitiesHandler.FlextTestsHandlerConfigParams]
        ] = FlextTestsFlextUtilitiesHandler.FlextTestsHandlerConfigParams


u = FlextTestsUtilities

__all__: list[str] = ["FlextTestsFixturesDSLMixin", "FlextTestsUtilities", "u"]
