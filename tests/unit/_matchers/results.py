"""Private matcher result assertion test mixins.

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

from collections.abc import Mapping
from re import escape

import pytest

from tests import c, m, p, r, t, tm


class TestsFlextTestsMatchersBooleanResultsMixin:
    """Boolean predicates and falsey result payload behavior."""

    @staticmethod
    def test_boolean_matchers_preserve_values_and_types() -> None:
        """Boolean predicates need no result wrapper and keep their type."""
        ok_value: bool = tm.ok(result=True)
        fail_value: bool = tm.fail(result=False)
        tm.that((ok_value, fail_value), eq=(True, False))
        tm.that(tm.ok(result=True), eq=True)
        tm.that(tm.fail(result=False), eq=False)

    @staticmethod
    def test_boolean_matchers_reject_opposite_states() -> None:
        """The migrated boolean assertions still detect actual failures."""
        with pytest.raises(AssertionError):
            tm.ok(result=False)
        with pytest.raises(AssertionError):
            tm.fail(result=True)

    @staticmethod
    def test_boolean_matchers_keep_custom_messages() -> None:
        """Predicate failures retain their caller's diagnostic message."""
        with pytest.raises(AssertionError, match="positive predicate"):
            tm.ok(result=False, msg="positive predicate")
        with pytest.raises(AssertionError, match="negative predicate"):
            tm.fail(result=True, msg="negative predicate")

    @staticmethod
    def test_boolean_matchers_reject_result_only_options() -> None:
        """Dynamic criteria cannot silently turn predicate checks into no-ops."""
        options: Mapping[str, str] = {"has": "error text"}
        with pytest.raises(ValueError, match="accept only msg"):
            tm.ok(result=True, **options)
        with pytest.raises(ValueError, match="accept only msg"):
            tm.fail(result=False, **options)

    @staticmethod
    @pytest.mark.parametrize("payload", [False, 0, "", [], {}])
    def test_successful_falsey_payload_is_not_a_failure(payload: t.JsonValue) -> None:
        """Result state, never payload truthiness, determines success."""
        result = r[t.JsonValue].ok(payload)
        tm.that(tm.ok(result) is payload, truth=True)
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            tm.fail(result)

    @staticmethod
    def test_none_is_rejected_by_result_construction_not_the_matcher() -> None:
        """Boolean support does not weaken the result owner's payload contract."""
        with pytest.raises(
            ValueError, match=escape(c.ERR_RESULT_SUCCESS_PAYLOAD_CANNOT_BE_NONE)
        ):
            r[t.JsonValue].ok(None)

    @staticmethod
    def test_false_payload_accepts_explicit_type_and_predicate_checks() -> None:
        """Successful False values keep result, type, and predicate semantics."""
        result = r[bool].ok(value=False)

        def is_false(value: object) -> bool:
            return value is False

        tm.that(tm.ok(result, is_=bool), eq=False)
        tm.that(tm.ok(result, where=is_false), eq=False)
        tm.that(tm.ok(result, eq=False), eq=False)
        tm.that(tm.ok(result, ne=True), eq=False)


class TestsFlextTestsMatchersResultsMixin(TestsFlextTestsMatchersBooleanResultsMixin):
    """Typed result and collection assertion tests."""

    @staticmethod
    def test_assert_result_success_passes() -> None:
        """Test tm.ok() with successful result."""
        result: p.Result[str] = r[str].ok("success")
        value: str = tm.ok(result)
        tm.that(value, eq="success")

    @staticmethod
    def test_ok_preserves_generic_result_payload() -> None:
        """The no-matcher overload preserves the producer's payload type."""
        result: p.Result[str] = r[str].ok("success")
        resolved: str = tm.ok(result)
        tm.that(resolved, eq="success")
        tm.that(tm.ok(result), eq="success")
        tm.that(
            tm.ok(r[t.JsonMapping].ok({"meta": {"id": "x"}}), path="meta.id"),
            eq="x",
        )

    @staticmethod
    def test_native_matchers_preserve_range_type_and_identity() -> None:
        """Native equality and typed predicates need no payload representation."""
        original = range(2, 9, 2)

        def has_same_step(value: range) -> bool:
            return value is original and value.step == original.step

        def has_same_start(value: range) -> bool:
            return value is original and value.start == original.start

        tm.that(original, eq=range(2, 9, 2), where=has_same_step)
        resolved: range = tm.ok(
            r[range].ok(original), eq=original, where=has_same_start
        )
        tm.that(resolved is original, truth=True)
        with pytest.raises(AssertionError):
            tm.that(original, eq=range(3))

        def has_single_step(value: range) -> bool:
            return value.step == 1

        with pytest.raises(AssertionError):
            tm.that(original, where=has_single_step)

    @staticmethod
    def test_structural_checks_preserve_original_collection() -> None:
        """Adding structural criteria never changes the success payload type."""
        original = [3, 1, 2]

        def keeps_original_head(values: list[int]) -> bool:
            return values is original and values[0] == original[0]

        resolved: list[int] = tm.ok(
            r[list[int]].ok(original),
            len=3,
            has=1,
            where=keeps_original_head,
        )
        tm.that(resolved is original, truth=True)

    @staticmethod
    def test_ok_preserves_arbitrary_result_payload() -> None:
        """The no-matcher overload accepts payloads outside the matcher union."""

        class Payload(m.BaseModel):
            value: str

        payload = Payload(value="typed")
        result = r[Payload].ok(payload)

        def is_original_payload(value: Payload) -> bool:
            return value is payload and value.value == "typed"

        resolved: Payload = tm.ok(result)
        tm.that(resolved, eq=payload)
        checked: Payload = tm.ok(result, eq=payload, where=is_original_payload)
        tm.that(checked is payload, truth=True)

    @staticmethod
    def test_assert_result_success_fails() -> None:
        """Test tm.ok() with failed result."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            tm.ok(result)

    @staticmethod
    def test_assert_result_success_custom_message() -> None:
        """Test tm.ok() with custom error message."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Custom message"):
            tm.ok(result, msg="Custom message")

    @staticmethod
    def test_assert_result_failure_passes() -> None:
        """Test tm.fail() with failed result."""
        result: p.Result[str] = r[str].fail("error")
        error = tm.fail(result)
        tm.that(error, eq="error")

    @staticmethod
    def test_assert_result_failure_fails() -> None:
        """Test tm.fail() with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            tm.fail(result)

    @staticmethod
    def test_assert_result_failure_with_expected_error() -> None:
        """Test tm.fail() with expected error substring."""
        result: p.Result[str] = r[str].fail("Database connection failed")
        error = tm.fail(result, contains="connection")
        tm.that(error, has="connection")

    @staticmethod
    def test_assert_result_failure_expected_error_not_found() -> None:
        """Test tm.fail() when expected error substring not found."""
        result: p.Result[str] = r[str].fail("Database error")
        with pytest.raises(AssertionError, match=r"Expected.*to contain 'connection'"):
            tm.fail(result, contains="connection")

    @staticmethod
    def test_assert_dict_contains_passes() -> None:
        """Test tm.that() with contains parameter for dict."""
        data = {"key1": "value1", "key2": "value2"}
        expected = {"key1": "value1"}
        tm.that(data, kv=expected)

    @staticmethod
    def test_assert_dict_contains_missing_key() -> None:
        """Test tm.that() with missing key."""
        data = {"key1": "value1"}
        expected = {"key2": "value2"}
        with pytest.raises(AssertionError, match="Key 'key2' not found in mapping"):
            tm.that(data, kv=expected)

    @staticmethod
    def test_assert_dict_contains_wrong_value() -> None:
        """Test tm.that() with wrong value."""
        data = {"key1": "value1"}
        expected = {"key1": "wrong_value"}
        with pytest.raises(
            AssertionError,
            match="expected 'wrong_value', got 'value1'",
        ):
            tm.that(data, kv=expected)

    @staticmethod
    def test_assert_list_contains_passes() -> None:
        """Test tm.that() with has parameter for list."""
        items = ["item1", "item2", "item3"]
        tm.that(items, has="item2")

    @staticmethod
    def test_assert_list_contains_missing_item() -> None:
        """Test tm.that() with item not in list."""
        items = ["item1", "item2"]
        with pytest.raises(AssertionError, match=r"Expected.*to contain 'item3'"):
            tm.that(items, has="item3")
