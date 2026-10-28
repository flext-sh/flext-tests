"""Exception for enforcement violations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class FlextTestsFixturesEnforcementError(Exception):
    """Raised by ``FlextTestsEnforcementItem.runtest`` when violations are present."""


__all__: list[str] = ["FlextTestsFixturesEnforcementError"]
