"""Mypy regression for result matcher diagnostics with nested rules."""

from __future__ import annotations

from flext_core import r
from flext_tests import tm


class TestsFlextTestsMypyMatcherRepro:
    """Retain the static matcher regression inside the canonical test namespace."""

    @staticmethod
    def exercise_nested_matcher_diagnostic() -> None:
        """Type-check a mismatched result assertion without recursive alias expansion."""
        # Mypy must accept this nested paths mapping without recursive alias expansion.
        tm.ok(r[int].ok(1), eq="wrong", paths={"value": {"eq": 2}})
