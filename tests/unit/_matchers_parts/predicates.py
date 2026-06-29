"""Private matcher predicate helpers."""

from __future__ import annotations

from tests import t


def is_string(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, str)


def is_string_or_bytes(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, str | bytes)


def is_positive(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, int) and value > 0


def is_negative(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, int) and value < 0


def greater_than_zero(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, int) and value > 0


def greater_than_two(value: t.Tests.TestobjectSerializable) -> bool:
    return isinstance(value, int) and value > 2
