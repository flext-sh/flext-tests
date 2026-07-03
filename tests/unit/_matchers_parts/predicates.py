"""Private matcher predicate helpers."""

from __future__ import annotations

from tests.typings import t


class MatchersPredicates:
    """Shared boolean predicates used as ``where=``/``all_=``/``any_=`` callables."""

    @staticmethod
    def is_string(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, str)

    @staticmethod
    def is_string_or_bytes(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, str | bytes)

    @staticmethod
    def is_positive(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, int) and value > 0

    @staticmethod
    def is_negative(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, int) and value < 0

    @staticmethod
    def greater_than_zero(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, int) and value > 0

    @staticmethod
    def greater_than_two(value: t.Tests.TestobjectSerializable) -> bool:
        return isinstance(value, int) and value > 2
