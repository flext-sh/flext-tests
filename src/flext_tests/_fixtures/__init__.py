# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures import _enforcement_parts
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
    from flext_tests._fixtures.namespace import run_namespace, test_namespace
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_tool_flext,
    )
    from flext_tests._fixtures.settings import (
        clean_container,
        reset_settings,
        sample_data,
        settings,
        settings_factory,
        temp_dir,
        temp_file,
        test_context,
        test_runtime,
    )


__all__: tuple[str, ...] = (
    "FlextTestsCapabilityPlugin",
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "_enforcement_parts",
    "clean_container",
    "project_metadata",
    "project_tool_flext",
    "reset_settings",
    "run_namespace",
    "sample_data",
    "settings",
    "settings_factory",
    "temp_dir",
    "temp_file",
    "test_context",
    "test_namespace",
    "test_runtime",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsCapabilityPlugin": ".connectivity",
        "FlextTestsEnforcementBuilder": "._enforcement_parts.build",
        "FlextTestsEnforcementDispatcher": "._enforcement_parts.dispatcher",
        "FlextTestsEnforcementItem": "._enforcement_parts.items",
        "FlextTestsEnforcementValidators": "._enforcement_parts.validators",
        "_enforcement_parts": "._enforcement_parts",
        "clean_container": ".settings",
        "project_metadata": ".project_metadata",
        "project_tool_flext": ".project_metadata",
        "reset_settings": ".settings",
        "run_namespace": ".namespace",
        "sample_data": ".settings",
        "settings": ".settings",
        "settings_factory": ".settings",
        "temp_dir": ".settings",
        "temp_file": ".settings",
        "test_context": ".settings",
        "test_namespace": ".namespace",
        "test_runtime": ".settings",
    }),
    public_exports=__all__,
)
