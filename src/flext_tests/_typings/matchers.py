"""Finite matcher types; recursive native contracts belong to payload protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from flext_core import t

if TYPE_CHECKING:
    from flext_tests import p


class FlextTestsMatchersTypesMixin:
    """Nonrecursive matcher scalar, selector, and callback shapes."""

    type LengthSpec = int | tuple[int, int]
    type ComparableScalar = float | int | str
    type ItemSelector = int | str
    type PathSpec = str | t.StrSequence
    type ExclusionSpec = str | t.StrSequence
    type KeySpec = t.StrSequence | set[str]
    type AttributeSpec = str | t.StrSequence
    type ErrorCodeSpec = str | t.StrSequence
    type CleanupSpec = t.SequenceOf[Callable[[], None]]
    type EnvironmentSpec = t.StrMapping

    type MatcherOption = (
        p.Tests.NativeMatchValue
        | p.Tests.Payload
        | t.RegexPattern
        | type
        | t.VariadicTuple[type]
        | Callable[[p.Tests.NativeMatchValue], bool]
        | Callable[[p.Tests.NativeMatchValue], p.Tests.NativeMatchValue]
        | t.MappingKV[
            str | int,
            p.Tests.NativeMatchValue
            | p.Tests.Payload
            | Callable[[p.Tests.NativeMatchValue], bool],
        ]
        | p.Tests.MatcherCriteriaMapping
        | p.Tests.MatcherCriteriaSequence
        | t.StrSequence
        | LengthSpec
    )
__all__: list[str] = ["FlextTestsMatchersTypesMixin"]
