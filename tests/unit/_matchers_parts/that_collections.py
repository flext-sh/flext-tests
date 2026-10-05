"""Private matcher that collection test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_tests import tm
from tests import c, t
from tests.unit._matchers_parts.predicates import TestsFlextTestsMatchersPredicates


class TestsFlextTestsMatchersThatCollectionsNarrowingMixin:
    """Narrowing tests for ``tm.that()`` value and None constraints."""

    @staticmethod
    def test_that_with_eq_parameter() -> None:
        """eq= accepts a computed equal value and rejects a different one."""
        tm.that(sum((40, 2)), eq=42)
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(sum((40, 2)), eq=43)

    @staticmethod
    def test_that_with_ne_parameter() -> None:
        """Test tm.that() with ne parameter."""
        tm.that(42, ne=43)

    @staticmethod
    def test_that_with_is_parameter() -> None:
        """Test tm.that() with is_ parameter."""
        tm.that("test", is_=str)

    @staticmethod
    def test_that_with_is_tuple_parameter() -> None:
        """Test tm.that() with is_ tuple parameter."""
        tm.that("test", is_=(str, bytes))

    @staticmethod
    def test_that_with_not_parameter() -> None:
        """Test tm.that() with not_ parameter."""
        tm.that("test", not_=int)

    @staticmethod
    def test_that_with_none_parameter() -> None:
        """Test tm.that() with none parameter."""
        tm.that("test", none=False)
        tm.that(None, none=True)

    @staticmethod
    def test_that_none_false_rejects_none() -> None:
        """none=False narrowing is fail-closed for None values."""
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(None, none=False)

    @staticmethod
    def test_that_is_type_rejects_none() -> None:
        """is_=type narrowing is fail-closed for None values."""
        with pytest.raises(AssertionError, match=r"Expected type .* but got NoneType"):
            tm.that(None, is_=dict)

    @staticmethod
    def test_that_eq_value_rejects_none() -> None:
        """eq=<value> narrowing is fail-closed for None values."""
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(None, eq="x")

    @staticmethod
    def test_that_eq_none_requires_none() -> None:
        """eq=None asserts the value is None instead of passing silently."""
        absent: t.StrMapping = {}
        tm.that(absent.get("missing"), eq=None)
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that("x", eq=None)

    @staticmethod
    def test_that_ne_none_requires_value() -> None:
        """ne=None asserts the value is not None instead of passing silently."""
        tm.that("x", ne=None)
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(None, ne=None)

    @staticmethod
    def test_not_none_returns_the_narrowed_value() -> None:
        """not_none returns the original value with its optional removed."""
        value: str | None = "test"
        tm.that(tm.not_none(value), eq="test")


class TestsFlextTestsMatchersThatCollectionsMixin(
    TestsFlextTestsMatchersThatCollectionsNarrowingMixin,
):
    """Matcher that collection tests."""

    @staticmethod
    def test_not_none_rejects_none_with_context() -> None:
        """not_none raises the caller-provided assertion context for None."""
        with pytest.raises(AssertionError, match="missing channel"):
            tm.not_none(None, msg="missing channel")

    @staticmethod
    def test_that_with_empty_parameter() -> None:
        """Test tm.that() with empty parameter."""
        tm.that(["a"], empty=False)
        tm.that([], empty=True)

    @staticmethod
    def test_that_with_has_parameter() -> None:
        """Test tm.that() with has parameter."""
        tm.that(["a", "b", "c"], has="a")

    @staticmethod
    def test_that_with_has_parameter_supports_strenum_sets() -> None:
        """Test tm.that() containment with sets of StrEnum values."""
        tm.that(
            {c.Tests.FILE_FORMAT_TEXT, c.Tests.FILE_FORMAT_BIN},
            has=c.Tests.FILE_FORMAT_TEXT,
        )

    @staticmethod
    def test_that_with_has_sequence_parameter() -> None:
        """Test tm.that() with has sequence parameter."""
        tm.that(["a", "b", "c"], has=["a", "b"])

    @staticmethod
    def test_that_with_lacks_parameter() -> None:
        """Test tm.that() with lacks parameter."""
        tm.that(["a", "b", "c"], lacks="d")

    @staticmethod
    def test_that_with_lacks_preserves_whitespace_only_string() -> None:
        """Keep whitespace-only exclusion needles unchanged by model parsing."""
        tm.that("a\n\nb", lacks="\n\n\n\n")

    @staticmethod
    def test_that_with_first_parameter() -> None:
        """Test tm.that() with first parameter."""
        tm.that(["a", "b", "c"], first="a")

    @staticmethod
    def test_that_with_last_parameter() -> None:
        """Test tm.that() with last parameter."""
        tm.that(["a", "b", "c"], last="c")

    @staticmethod
    def test_that_with_all_type_parameter() -> None:
        """Test tm.that() with all_ type parameter."""
        tm.that(["a", "b", "c"], all_=str)

    @staticmethod
    def test_that_with_all_predicate_parameter() -> None:
        """Test tm.that() with all_ predicate parameter."""
        tm.that([1, 2, 3], all_=TestsFlextTestsMatchersPredicates.greater_than_zero)

    @staticmethod
    def test_that_with_any_type_parameter() -> None:
        """Test tm.that() with any_ type parameter."""
        tm.that(["a", 1, "c"], any_=int)

    @staticmethod
    def test_that_with_any_predicate_parameter() -> None:
        """Test tm.that() with any_ predicate parameter."""
        tm.that([1, 2, 3], any_=TestsFlextTestsMatchersPredicates.greater_than_two)

    @staticmethod
    def test_that_with_sorted_parameter() -> None:
        """Test tm.that() with sorted parameter."""
        tm.that([1, 2, 3], sorted=True)

    @staticmethod
    def test_that_with_unique_parameter() -> None:
        """Test tm.that() with unique parameter."""
        tm.that([1, 2, 3], unique=True)

    @staticmethod
    def test_that_with_keys_parameter() -> None:
        """Test tm.that() with keys parameter."""
        tm.that({"a": 1, "b": 2}, keys=["a", "b"])

    @staticmethod
    def test_that_with_lacks_keys_parameter() -> None:
        """Test tm.that() with lacks_keys parameter."""
        tm.that({"a": 1}, lacks_keys=["b"])

    @staticmethod
    def test_that_with_values_parameter() -> None:
        """Test tm.that() with values parameter."""
        tm.that({"a": 1, "b": 2}, values=[1, 2])

    @staticmethod
    def test_that_with_kv_tuple_parameter() -> None:
        """Test tm.that() with kv tuple parameter."""
        tm.that({"a": 1}, kv=("a", 1))

    @staticmethod
    def test_that_with_kv_mapping_parameter() -> None:
        """Test tm.that() with kv mapping parameter."""
        tm.that({"a": 1, "b": 2}, kv={"a": 1, "b": 2})
