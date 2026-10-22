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
    from flext_tests._fixtures import _enforcement as _enforcement
    from flext_tests._fixtures._enforcement import (
        FlextTestsEnforcementBuilder,
        FlextTestsEnforcementCollector,
        FlextTestsEnforcementDispatcher,
        FlextTestsEnforcementItem,
        FlextTestsEnforcementValidators,
        FlextTestsEnforcementViolationError,
    )
    from flext_tests._fixtures.connectivity import FlextTestsCapabilityPlugin
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_tool_flext,
    )
    from flext_tests._fixtures.scratch_storage import FlextTestsScratchStoragePlugin


__all__: tuple[str, ...] = (
    "FlextTestsCapabilityPlugin",
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementCollector",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "FlextTestsEnforcementViolationError",
    "FlextTestsScratchStoragePlugin",
    "_enforcement",
    "project_metadata",
    "project_tool_flext",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsCapabilityPlugin": ".connectivity",
        "FlextTestsEnforcementBuilder": "._enforcement.build",
        "FlextTestsEnforcementCollector": "._enforcement._collector",
        "FlextTestsEnforcementDispatcher": "._enforcement.dispatcher",
        "FlextTestsEnforcementItem": "._enforcement.items",
        "FlextTestsEnforcementValidators": "._enforcement.validators",
        "FlextTestsEnforcementViolationError": "._enforcement._error",
        "FlextTestsScratchStoragePlugin": ".scratch_storage",
        "_enforcement": "._enforcement",
        "project_metadata": ".project_metadata",
        "project_tool_flext": ".project_metadata",
    }),
    public_exports=__all__,
)
