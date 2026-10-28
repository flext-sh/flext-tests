"""Mypy regression for result matcher diagnostics with nested rules.

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

from tests import r, tm


class TestsFlextTestsMypyMatcherRepro:
    """Retain the static matcher regression inside the canonical test namespace."""

    @staticmethod
    def exercise_nested_matcher_diagnostic() -> None:
        """Type-check a mismatched result assertion.

        Without recursive alias expansion.
        """
        # Mypy must accept this nested paths mapping without recursive alias expansion.
        tm.ok(r[int].ok(1), eq="wrong", paths={"value": {"eq": 2}})
