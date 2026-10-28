"""Private matcher predicate helpers.

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

from typing import Final

from tests import p

GREATER_THAN_TWO_THRESHOLD: Final[int] = 2


class TestsFlextTestsMatchersPredicates:
    """Shared boolean predicates used as ``where=``/``all_=``/``any_=`` callables."""

    @staticmethod
    def is_string(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, str)

    @staticmethod
    def is_string_or_bytes(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, str | bytes)

    @staticmethod
    def is_positive(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, int) and value > 0

    @staticmethod
    def is_negative(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, int) and value < 0

    @staticmethod
    def greater_than_zero(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, int) and value > 0

    @staticmethod
    def greater_than_two(value: p.Tests.NativeMatchValue) -> bool:
        return isinstance(value, int) and value > GREATER_THAN_TWO_THRESHOLD
