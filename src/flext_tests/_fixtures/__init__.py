# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures import _enforcement_parts
    from flext_tests._fixtures._enforcement_parts._collector import (
        FlextTestsEnforcementCollector,
    )
    from flext_tests._fixtures._enforcement_parts._error import (
        FlextTestsEnforcementViolationError,
    )
    from flext_tests._fixtures._enforcement_parts.build import (
        FlextTestsEnforcementBuilder,
    )
    from flext_tests._fixtures._enforcement_parts.dispatcher import (
        FlextTestsEnforcementDispatcher,
    )
    from flext_tests._fixtures._enforcement_parts.items import FlextTestsEnforcementItem
    from flext_tests._fixtures._enforcement_parts.validators import (
        FlextTestsEnforcementValidators,
    )
    from flext_tests._fixtures.connectivity import FlextTestsCapabilityPlugin
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_tool_flext,
    )
    from flext_tests._fixtures.scratch_storage import pytest_addoption, pytest_configure


__all__: tuple[str, ...] = (
    "FlextTestsCapabilityPlugin",
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementCollector",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "FlextTestsEnforcementViolationError",
    "_enforcement_parts",
    "project_metadata",
    "project_tool_flext",
    "pytest_addoption",
    "pytest_configure",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsCapabilityPlugin": ".connectivity",
        "FlextTestsEnforcementBuilder": "._enforcement_parts.build",
        "FlextTestsEnforcementCollector": "._enforcement_parts._collector",
        "FlextTestsEnforcementDispatcher": "._enforcement_parts.dispatcher",
        "FlextTestsEnforcementItem": "._enforcement_parts.items",
        "FlextTestsEnforcementValidators": "._enforcement_parts.validators",
        "FlextTestsEnforcementViolationError": "._enforcement_parts._error",
        "_enforcement_parts": "._enforcement_parts",
        "project_metadata": ".project_metadata",
        "project_tool_flext": ".project_metadata",
        "pytest_addoption": ".scratch_storage",
        "pytest_configure": ".scratch_storage",
    }),
    public_exports=__all__,
)
