"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from pydantic import BaseModel

from flext_tests import (
    m,
    t,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsDeepMatchUtilitiesMixin:
    """Deep structural matching utilities - delegates to FlextCliUtilities.extract().

    Follows FLEXT patterns:
    - Zero code duplication - delegates to flext-core utilities
    - Uses t.Tests.DeepSpec for type safety
    - Returns m.Tests.DeepMatchResult for structured results
    - Supports unlimited nesting depth via dot notation

    All operations delegate to FlextCliUtilities.extract() for
    path extraction, ensuring consistency with flext-core patterns.
    """

    @staticmethod
    def match(
        obj: BaseModel | Mapping[str, t.Tests.TestobjectSerializable],
        spec: t.Tests.DeepSpec,
        *,
        path_sep: str = ".",
    ) -> m.Tests.DeepMatchResult:
        """Match t.NormalizedValue against deep specification.

        Uses FlextCliUtilities.extract() for path extraction - NO code duplication.
        Supports unlimited nesting depth via dot notation paths.

        Args:
            obj: Object to match against (dict or Pydantic model)
            spec: DeepSpec mapping of path -> expected value or predicate
            path_sep: Path separator (default: ".")

        Returns:
            r[TEntity]: Result containing created entity or error
            DeepMatchResult with match status and details

        Examples:
            result = FlextCliUtilities.Tests.DeepMatch.match(
                data,
                {
                    "user.name": "John",
                    "user.email": lambda e: "@" in e,
                    "user.profile.age": 25,
                }
            )
            if not result.matched:
                raise AssertionError(f"Failed at {result.path}: {result.reason}")

        """
        return FlextTestsPayloadUtilities.deep_match(obj, spec, path_sep=path_sep)
