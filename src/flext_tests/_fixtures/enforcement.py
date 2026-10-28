"""Extracted facade class for enforcement.

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

from flext_tests._fixtures._enforcement import (
    FlextTestsEnforcementBuilder,
    FlextTestsEnforcementDispatcher,
    FlextTestsEnforcementItem,
    FlextTestsEnforcementValidators,
    FlextTestsFixturesEnforcementCollector,
)


class FlextTestsFixturesEnforcement(
    FlextTestsEnforcementBuilder,
    FlextTestsEnforcementDispatcher,
    FlextTestsEnforcementItem,
    FlextTestsEnforcementValidators,
    FlextTestsFixturesEnforcementCollector,
):
    """Facade for enforcement."""


__all__: list[str] = ["FlextTestsFixturesEnforcement"]
