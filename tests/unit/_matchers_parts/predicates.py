"""Private matcher predicate helpers."""

from __future__ import annotations

from tests import p


class TestsFlextTestsMatchersPredicates:
    """Shared boolean predicates used as ``where=``/``all_=``/``any_=`` callables."""

    @staticmethod
    def is_string(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, str)

    @staticmethod
    def is_string_or_bytes(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, str | bytes)

    @staticmethod
    def is_positive(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, int) and value.atom > 0

    @staticmethod
    def is_negative(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, int) and value.atom < 0

    @staticmethod
    def greater_than_zero(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, int) and value.atom > 0

    @staticmethod
    def greater_than_two(value: p.Tests.Payload) -> bool:
        return isinstance(value.atom, int) and value.atom > 2
