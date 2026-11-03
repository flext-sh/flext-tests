# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures.connectivity import FlextTestsCapabilityPlugin
    from flext_tests._fixtures.enforcement import FlextTestsFixturesEnforcement
    from flext_tests._fixtures.fixture_trees import FlextTestsFixtureTreesFixtures
    from flext_tests._fixtures.namespace import FlextTestsNamespaceFixtures
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_tool_flext,
    )
    from flext_tests._fixtures.scratch_storage import FlextTestsScratchStoragePlugin
    from flext_tests._fixtures.settings import FlextTestsSettingsFixtures


__all__: tuple[str, ...] = (
    "FlextTestsCapabilityPlugin",
    "FlextTestsFixtureTreesFixtures",
    "FlextTestsFixturesEnforcement",
    "FlextTestsNamespaceFixtures",
    "FlextTestsScratchStoragePlugin",
    "FlextTestsSettingsFixtures",
    "project_metadata",
    "project_tool_flext",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsCapabilityPlugin": ".connectivity",
        "FlextTestsFixtureTreesFixtures": ".fixture_trees",
        "FlextTestsFixturesEnforcement": ".enforcement",
        "FlextTestsNamespaceFixtures": ".namespace",
        "FlextTestsScratchStoragePlugin": ".scratch_storage",
        "FlextTestsSettingsFixtures": ".settings",
        "project_metadata": ".project_metadata",
        "project_tool_flext": ".project_metadata",
    },
    public_exports=__all__,
)
