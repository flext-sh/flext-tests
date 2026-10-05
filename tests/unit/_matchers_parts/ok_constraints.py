"""Private matcher ok constraint test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_tests import r, tm
from tests import t
from tests.unit._matchers_parts.predicates import TestsFlextTestsMatchersPredicates


class TestsFlextTestsMatchersOkConstraintsContentMixin:
    """Matcher ok content and structure constraint tests."""

    @staticmethod
    def test_ok_with_is_parameter() -> None:
        """Test tm.ok() with is_ parameter."""
        result = r[str].ok("test")
        value = tm.ok(result, where=TestsFlextTestsMatchersPredicates.is_string)
        tm.that(value, eq="test")

    @staticmethod
    def test_ok_with_is_tuple_parameter() -> None:
        """Test tm.ok() with is_ tuple parameter."""
        result = r[str].ok("test")
        value = tm.ok(
            result,
            where=TestsFlextTestsMatchersPredicates.is_string_or_bytes,
        )
        tm.that(value, eq="test")

    @staticmethod
    def test_ok_with_has_parameter() -> None:
        """Test tm.ok() with has parameter."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, has="a")
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_ok_with_has_sequence_parameter() -> None:
        """Test tm.ok() with has sequence parameter."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, has=["a", "b"])
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_ok_with_lacks_parameter() -> None:
        """Test tm.ok() with lacks parameter."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, lacks="d")
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_ok_with_len_exact_parameter() -> None:
        """Test tm.ok() with len exact parameter."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, len=3)
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_ok_with_len_range_parameter() -> None:
        """Test tm.ok() with len range parameter."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, len=(2, 4))
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_ok_with_deep_parameter() -> None:
        """Test tm.ok() with deep parameter."""
        data: t.JsonMapping = {"user": {"name": "John", "age": 30}}
        result = r[t.JsonMapping].ok(data)
        value = tm.ok(result, deep={"user.name": "John"})
        tm.that(value, eq=data)

    @staticmethod
    def test_ok_with_deep_predicate_parameter() -> None:
        """Test tm.ok() with deep predicate parameter."""
        data: t.JsonMapping = {"user": {"email": "test@example.com"}}
        result = r[t.JsonMapping].ok(data)
        value = tm.ok(
            result,
            deep={"user.email": TestsFlextTestsMatchersPredicates.is_string},
        )
        tm.that(value, eq=data)

    @staticmethod
    def test_ok_with_missing_deep_predicate_path_fails_cleanly() -> None:
        """Report a missing predicate path through the public matcher contract."""
        data: t.JsonMapping = {"user": {"email": "test@example.com"}}
        result = r[t.JsonMapping].ok(data)
        with pytest.raises(AssertionError, match=r"Path not found: user.missing"):
            tm.ok(
                result,
                deep={"user.missing": TestsFlextTestsMatchersPredicates.is_string},
            )


class TestsFlextTestsMatchersOkConstraintsMixin(
    TestsFlextTestsMatchersOkConstraintsContentMixin,
):
    """Matcher ok constraint tests."""

    @staticmethod
    def test_ok_with_path_parameter() -> None:
        """Test tm.ok() with path parameter."""
        data: t.JsonMapping = {"user": {"name": "John"}}
        result = r[t.JsonMapping].ok(data)
        value = tm.ok(result, path="user.name", eq="John")
        tm.that(value, eq="John")

    @staticmethod
    def test_ok_with_where_parameter() -> None:
        """Test tm.ok() with where parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, where=TestsFlextTestsMatchersPredicates.is_positive)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_where_parameter_fails() -> None:
        """Test tm.ok() with where parameter fails when predicate returns False."""
        result = r[int].ok(42)
        with pytest.raises(AssertionError):
            tm.ok(result, where=TestsFlextTestsMatchersPredicates.is_negative)

    @staticmethod
    def test_ok_with_starts_parameter() -> None:
        """Test tm.ok() with starts parameter."""
        result = r[str].ok("Hello World")
        value = tm.ok(result, starts="Hello")
        tm.that(value, eq="Hello World")

    @staticmethod
    def test_ok_with_ends_parameter() -> None:
        """Test tm.ok() with ends parameter."""
        result = r[str].ok("Hello World")
        value = tm.ok(result, ends="World")
        tm.that(value, eq="Hello World")

    @staticmethod
    def test_ok_with_match_parameter() -> None:
        """Test tm.ok() with match parameter."""
        result = r[str].ok("test@example.com")
        value = tm.ok(result, match="^[\\w.]+@[\\w.]+$")
        tm.that(value, eq="test@example.com")

    @staticmethod
    def test_ok_with_gt_parameter() -> None:
        """Test tm.ok() with gt parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, gt=0)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_gte_parameter() -> None:
        """Test tm.ok() with gte parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, gte=42)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_lt_parameter() -> None:
        """Test tm.ok() with lt parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, lt=100)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_lte_parameter() -> None:
        """Test tm.ok() with lte parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, lte=42)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_none_parameter() -> None:
        """Test tm.ok() with none parameter."""
        result = r[str | None].ok("test")
        value = tm.ok(result, none=False)
        tm.that(value, eq="test")

    @staticmethod
    def test_ok_with_empty_parameter() -> None:
        """Test tm.ok() with empty parameter."""
        result = r[t.StrSequence].ok(["a"])
        value = tm.ok(result, empty=False)
        tm.that(value, eq=["a"])
