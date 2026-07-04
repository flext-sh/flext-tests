"""Private matcher that attribute test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from flext_tests import r, tm
from tests.unit._matchers_parts.predicates import MatchersPredicates

if TYPE_CHECKING:
    from tests.protocols import p
    from tests.typings import t


class MatchersThatAttrsMixin:
    """Matcher that attribute tests."""

    def test_that_with_attrs_parameter(self) -> None:
        """Test tm.that() with attrs parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = TestClass()
        tm.that(cast("t.JsonValue", obj), attrs=["attr1", "attr2"])

    def test_that_with_methods_parameter(self) -> None:
        """Test tm.that() with methods parameter."""

        class TestClass:
            def method1(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            def method2(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

        obj = TestClass()
        tm.that(cast("t.JsonValue", obj), methods=["method1", "method2"])

    def test_that_with_attr_eq_tuple_parameter(self) -> None:
        """Test tm.that() with attr_eq tuple parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr = "value"

        obj = TestClass()
        tm.that(cast("t.JsonValue", obj), attr_eq=("attr", "value"))

    def test_that_with_attr_eq_mapping_parameter(self) -> None:
        """Test tm.that() with attr_eq mapping parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = TestClass()
        tm.that(
            cast("t.JsonValue", obj),
            attr_eq={"attr1": "value1", "attr2": "value2"},
        )

    def test_that_with_ok_parameter(self) -> None:
        """Test tm.that() with ok parameter for r."""
        result = r[str].ok("success")
        tm.that(result, ok=True)

    def test_that_with_error_parameter(self) -> None:
        """Test tm.that() with error parameter for r."""
        result: p.Result[str] = r[str].fail("error")
        tm.that(result, error="error")

    def test_that_with_deep_parameter(self) -> None:
        """Test tm.that() with deep parameter."""
        data: t.MappingKV[str, t.Tests.TestobjectSerializable] = {
            "user": {"name": "John", "age": 30},
        }
        tm.that(data, deep={"user.name": "John"})

    def test_that_with_where_parameter(self) -> None:
        """Test tm.that() with where parameter."""
        tm.that(42, where=MatchersPredicates.is_positive)

    def test_that_with_all_alias_parameter(self) -> None:
        """Test tm.that() with all alias parameter (accepts both all_ and all)."""
        tm.that(["a", "b", "c"], all=str)

    def test_that_with_any_alias_parameter(self) -> None:
        """Test tm.that() with any alias parameter (accepts both any_ and any)."""
        tm.that(["a", 1, "c"], any=int)
