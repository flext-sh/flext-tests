# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for fixtures.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures.connectivity import FlextTestsCapabilityPlugin
    from flext_tests._fixtures.enforcement import FlextTestsFixturesEnforcement
    from flext_tests._fixtures.fixture_trees import FlextTestsFixtureTreesFixtures
    from flext_tests._fixtures.namespace import FlextTestsNamespaceFixtures
    from flext_tests._fixtures.scratch_storage import FlextTestsScratchStoragePlugin
    from flext_tests._fixtures.settings import FlextTestsSettingsFixtures

__all__: tuple[str, ...] = (
    "FlextTestsCapabilityPlugin",
    "FlextTestsFixtureTreesFixtures",
    "FlextTestsFixturesEnforcement",
    "FlextTestsNamespaceFixtures",
    "FlextTestsScratchStoragePlugin",
    "FlextTestsSettingsFixtures",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsCapabilityPlugin": ".connectivity",
        "FlextTestsFixtureTreesFixtures": ".fixture_trees",
        "FlextTestsFixturesEnforcement": ".enforcement",
        "FlextTestsNamespaceFixtures": ".namespace",
        "FlextTestsScratchStoragePlugin": ".scratch_storage",
        "FlextTestsSettingsFixtures": ".settings",
    }),
    public_exports=__all__,
)
