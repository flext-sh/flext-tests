"""Finite matcher types; recursive native contracts belong to payload protocols."""

from __future__ import annotations

from collections.abc import Callable

from flext_core import t


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
