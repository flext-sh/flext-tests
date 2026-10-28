"""Extracted facade class for fixtures.

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

from flext_tests._fixtures import (
    FlextTestsCapabilityPlugin,
    FlextTestsFixturesEnforcement,
    FlextTestsFixtureTreesFixtures,
    FlextTestsNamespaceFixtures,
    FlextTestsScratchStoragePlugin,
    FlextTestsSettingsFixtures,
)


class FlextTestsFlextTestsFixtures(
    FlextTestsCapabilityPlugin,
    FlextTestsFixtureTreesFixtures,
    FlextTestsFixturesEnforcement,
    FlextTestsNamespaceFixtures,
    FlextTestsScratchStoragePlugin,
    FlextTestsSettingsFixtures,
):
    """Facade for fixtures."""


__all__: list[str] = ["FlextTestsFlextTestsFixtures"]
