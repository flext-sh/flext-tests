"""Extracted facade class for enforcement.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests._fixtures._enforcement import (
    FlextTestsEnforcementBuilder,
    FlextTestsEnforcementDispatcher,
    FlextTestsEnforcementItem,
    FlextTestsEnforcementValidators,
    FlextTestsFixturesEnforcementCollector,
    FlextTestsFixturesEnforcementError,
)


class FlextTestsFixturesEnforcement(
    FlextTestsEnforcementBuilder,
    FlextTestsEnforcementDispatcher,
    FlextTestsEnforcementItem,
    FlextTestsEnforcementValidators,
    FlextTestsFixturesEnforcementCollector,
    FlextTestsFixturesEnforcementError,
):
    """Facade for enforcement."""


__all__: list[str] = ["FlextTestsFixturesEnforcement"]
