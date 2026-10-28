"""Exception for enforcement violations.

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


class FlextTestsFixturesEnforcementError(Exception):
    """Raised by ``FlextTestsEnforcementItem.runtest`` when violations are present."""


__all__: list[str] = ["FlextTestsFixturesEnforcementError"]
