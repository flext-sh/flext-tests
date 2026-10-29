"""Finite matcher types; recursive native contracts belong to payload protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence


class FlextTestsTypesMatchers:
    """Nonrecursive matcher scalar, selector, and callback shapes."""

    type LengthSpec = int | tuple[int, int]
    type ComparableScalar = float | int | str
    type ItemSelector = int | str
    type PathSpec = str | Sequence[str]
    type ExclusionSpec = str | Sequence[str]
    type KeySpec = Sequence[str] | set[str]
    type AttributeSpec = str | Sequence[str]
    type ErrorCodeSpec = str | Sequence[str]
    type CleanupSpec = Sequence[Callable[[], None]]
    type EnvironmentSpec = Mapping[str, str]


__all__: list[str] = ["FlextTestsTypesMatchers"]
