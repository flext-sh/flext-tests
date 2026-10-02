"""Private matcher that attribute test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_tests import tm
from tests import p, r, t
from tests.unit._matchers_parts.predicates import TestsFlextTestsMatchersPredicates


class TestsFlextTestsMatchersThatAttrsMixin:
    """Matcher that attribute tests."""

    @staticmethod
    def test_that_with_attrs_parameter() -> None:
        """Test tm.that() with attrs parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = TestClass()
        tm.that(obj, attrs=["attr1", "attr2"])

    @staticmethod
    def test_that_with_methods_parameter() -> None:
        """Test tm.that() with methods parameter."""

        class TestClass:
            def method1(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

            def method2(self) -> None:
                msg = "Must use unified test helpers per Rule 3.6"
                raise NotImplementedError(msg)

        obj = TestClass()
        tm.that(obj, methods=["method1", "method2"])

    @staticmethod
    def test_that_with_attr_eq_tuple_parameter() -> None:
        """Test tm.that() with attr_eq tuple parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr = "value"

        obj = TestClass()
        tm.that(obj, attr_eq=("attr", "value"))

    @staticmethod
    def test_that_with_attr_eq_mapping_parameter() -> None:
        """Test tm.that() with attr_eq mapping parameter."""

        class TestClass:
            def __init__(self) -> None:
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = TestClass()
        tm.that(obj, attr_eq={"attr1": "value1", "attr2": "value2"})

    @staticmethod
    def test_that_with_ok_parameter() -> None:
        """Test tm.that() with ok parameter for r."""
        result = r[str].ok("success")
        tm.that(result, ok=True)

    @staticmethod
    def test_that_with_error_parameter() -> None:
        """Test tm.that() with error parameter for r."""
        result: p.Result[str] = r[str].fail("error")
        tm.that(result, error="error")

    @staticmethod
    def test_that_with_deep_parameter() -> None:
        """Test tm.that() with deep parameter."""
        data: t.MappingKV[str, t.Tests.TestobjectSerializable] = {
            "user": {"name": "John", "age": 30},
        }
        tm.that(data, deep={"user.name": "John"})

    @staticmethod
    def test_that_with_deep_parameter_rejects_mismatch() -> None:
        """A deep literal expectation fails when the value at the path differs."""
        data: t.MappingKV[str, t.Tests.TestobjectSerializable] = {
            "user": {"name": "John"},
        }
        with pytest.raises(AssertionError, match="Value mismatch"):
            tm.that(data, deep={"user.name": "Jane"})

    @staticmethod
    def test_that_with_where_parameter() -> None:
        """Test tm.that() with where parameter."""
        tm.that(42, where=TestsFlextTestsMatchersPredicates.is_positive)

    @staticmethod
    def test_that_where_predicate_receives_the_native_value() -> None:
        """A predicate sees the value itself, so a falsy subject fails ``bool``."""
        tm.that(True, where=bool)
        with pytest.raises(AssertionError, match="Custom predicate failed"):
            tm.that(False, where=bool)

    @staticmethod
    def test_that_presence_checks_accept_any_runtime_object() -> None:
        """none=/is_=/ne=None hold for objects outside the payload vocabulary."""

        class Connection:
            """A runtime handle with no payload representation."""

        conn = Connection()
        tm.that(conn, none=False)
        tm.that(conn, ne=None)
        tm.that(conn, none=False, is_=Connection)
        tm.that(tm.ok(r[Connection].ok(conn), none=False) is conn, eq=True)
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(conn, none=True)

    @staticmethod
    def test_that_with_all_alias_parameter() -> None:
        """Test tm.that() with all alias parameter (accepts both all_ and all)."""
        tm.that(["a", "b", "c"], all=str)

    @staticmethod
    def test_that_with_any_alias_parameter() -> None:
        """Test tm.that() with any alias parameter (accepts both any_ and any)."""
        tm.that(["a", 1, "c"], any=int)
