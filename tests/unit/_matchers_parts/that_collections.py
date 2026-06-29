"""Private matcher that collection test mixins."""

from __future__ import annotations

from flext_tests import tm
from tests import c
from tests.unit._matchers_parts.predicates import (
    greater_than_two,
    greater_than_zero,
)


class MatchersThatCollectionsMixin:
    """Matcher that collection tests."""

    def test_that_with_eq_parameter(self) -> None:
        """Test tm.that() with eq parameter."""
        tm.that(42, eq=42)

    def test_that_with_ne_parameter(self) -> None:
        """Test tm.that() with ne parameter."""
        tm.that(42, ne=43)

    def test_that_with_is_parameter(self) -> None:
        """Test tm.that() with is_ parameter."""
        tm.that("test", is_=str)

    def test_that_with_is_tuple_parameter(self) -> None:
        """Test tm.that() with is_ tuple parameter."""
        tm.that("test", is_=(str, bytes))

    def test_that_with_not_parameter(self) -> None:
        """Test tm.that() with not_ parameter."""
        tm.that("test", not_=int)

    def test_that_with_none_parameter(self) -> None:
        """Test tm.that() with none parameter."""
        tm.that("test", none=False)
        tm.that(None, none=True)

    def test_that_with_empty_parameter(self) -> None:
        """Test tm.that() with empty parameter."""
        tm.that(["a"], empty=False)
        tm.that([], empty=True)

    def test_that_with_has_parameter(self) -> None:
        """Test tm.that() with has parameter."""
        tm.that(["a", "b", "c"], has="a")

    def test_that_with_has_parameter_supports_strenum_sets(self) -> None:
        """Test tm.that() containment with sets of StrEnum values."""
        tm.that(
            {c.Tests.FILE_FORMAT_TEXT, c.Tests.FILE_FORMAT_BIN},
            has=c.Tests.FILE_FORMAT_TEXT,
        )

    def test_that_with_has_sequence_parameter(self) -> None:
        """Test tm.that() with has sequence parameter."""
        tm.that(["a", "b", "c"], has=["a", "b"])

    def test_that_with_lacks_parameter(self) -> None:
        """Test tm.that() with lacks parameter."""
        tm.that(["a", "b", "c"], lacks="d")

    def test_that_with_first_parameter(self) -> None:
        """Test tm.that() with first parameter."""
        tm.that(["a", "b", "c"], first="a")

    def test_that_with_last_parameter(self) -> None:
        """Test tm.that() with last parameter."""
        tm.that(["a", "b", "c"], last="c")

    def test_that_with_all_type_parameter(self) -> None:
        """Test tm.that() with all_ type parameter."""
        tm.that(["a", "b", "c"], all_=str)

    def test_that_with_all_predicate_parameter(self) -> None:
        """Test tm.that() with all_ predicate parameter."""
        tm.that([1, 2, 3], all_=greater_than_zero)

    def test_that_with_any_type_parameter(self) -> None:
        """Test tm.that() with any_ type parameter."""
        tm.that(["a", 1, "c"], any_=int)

    def test_that_with_any_predicate_parameter(self) -> None:
        """Test tm.that() with any_ predicate parameter."""
        tm.that([1, 2, 3], any_=greater_than_two)

    def test_that_with_sorted_parameter(self) -> None:
        """Test tm.that() with sorted parameter."""
        tm.that([1, 2, 3], sorted=True)

    def test_that_with_unique_parameter(self) -> None:
        """Test tm.that() with unique parameter."""
        tm.that([1, 2, 3], unique=True)

    def test_that_with_keys_parameter(self) -> None:
        """Test tm.that() with keys parameter."""
        tm.that({"a": 1, "b": 2}, keys=["a", "b"])

    def test_that_with_lacks_keys_parameter(self) -> None:
        """Test tm.that() with lacks_keys parameter."""
        tm.that({"a": 1}, lacks_keys=["b"])

    def test_that_with_values_parameter(self) -> None:
        """Test tm.that() with values parameter."""
        tm.that({"a": 1, "b": 2}, values=[1, 2])

    def test_that_with_kv_tuple_parameter(self) -> None:
        """Test tm.that() with kv tuple parameter."""
        tm.that({"a": 1}, kv=("a", 1))

    def test_that_with_kv_mapping_parameter(self) -> None:
        """Test tm.that() with kv mapping parameter."""
        tm.that({"a": 1, "b": 2}, kv={"a": 1, "b": 2})
