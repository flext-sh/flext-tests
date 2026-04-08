"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_tests import (
    FlextTestsPayloadUtilities,
    t,
)


class FlextTestsLengthUtilitiesMixin:
    """Length validation utilities - delegates to FlextCliUtilities.chk().

    Follows FLEXT patterns:
    - Zero code duplication - delegates to flext-core utilities
    - Uses t.Tests.LengthSpec for type safety
    - Supports exact length or range validation
    - Works with any t.NormalizedValue that has __len__

    All operations delegate to FlextCliUtilities.chk() for validation,
    ensuring consistency with flext-core patterns.
    """

    @staticmethod
    def validate(
        value: t.Tests.TestobjectSerializable,
        spec: int | tuple[int, int],
    ) -> bool:
        """Validate length against spec.

        Uses FlextCliUtilities.chk() for validation - NO code duplication.
        Supports exact length (int) or range (tuple[int, int]).

        Args:
            value: Value to check length of (must have __len__)
            spec: LengthSpec - exact int or (min, max) tuple

        Returns:
            r[TEntity]: Result containing created entity or error
            True if length matches spec, False otherwise

        Examples:
            FlextCliUtilities.Tests.Length.validate("hello", 5)           # Exact: True
            FlextCliUtilities.Tests.Length.validate([1, 2, 3], (1, 10))  # Range: True
            FlextCliUtilities.Tests.Length.validate("hi", 5)              # Exact: False

        """
        return FlextTestsPayloadUtilities.length_validate(value, spec)
