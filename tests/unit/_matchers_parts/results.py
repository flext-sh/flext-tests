"""Private matcher result assertion test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import r, tm

if TYPE_CHECKING:
    from tests import p
    from tests import t


class MatchersResultsMixin:
    """Matcher result assertion tests."""

    def test_assert_result_success_passes(self) -> None:
        """Test tm.ok() with successful result."""
        result = r[str].ok("success")
        value: t.Tests.TestobjectSerializable = tm.ok(result)
        tm.that(value, eq="success")

    def test_assert_result_success_fails(self) -> None:
        """Test tm.ok() with failed result."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            tm.ok(result)

    def test_assert_result_success_custom_message(self) -> None:
        """Test tm.ok() with custom error message."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Custom message"):
            tm.ok(result, msg="Custom message")

    def test_assert_result_failure_passes(self) -> None:
        """Test tm.fail() with failed result."""
        result: p.Result[str] = r[str].fail("error")
        error = tm.fail(result)
        tm.that(error, eq="error")

    def test_assert_result_failure_fails(self) -> None:
        """Test tm.fail() with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            tm.fail(result)

    def test_assert_result_failure_with_expected_error(self) -> None:
        """Test tm.fail() with expected error substring."""
        result: p.Result[str] = r[str].fail("Database connection failed")
        error = tm.fail(result, contains="connection")
        tm.that(error, has="connection")

    def test_assert_result_failure_expected_error_not_found(self) -> None:
        """Test tm.fail() when expected error substring not found."""
        result: p.Result[str] = r[str].fail("Database error")
        with pytest.raises(AssertionError, match=r"Expected.*to contain 'connection'"):
            tm.fail(result, contains="connection")

    def test_assert_dict_contains_passes(self) -> None:
        """Test tm.that() with contains parameter for dict."""
        data = {"key1": "value1", "key2": "value2"}
        expected = {"key1": "value1"}
        tm.that(data, kv=expected)

    def test_assert_dict_contains_missing_key(self) -> None:
        """Test tm.that() with missing key."""
        data = {"key1": "value1"}
        expected = {"key2": "value2"}
        with pytest.raises(AssertionError, match="Key 'key2' not found in mapping"):
            tm.that(data, kv=expected)

    def test_assert_dict_contains_wrong_value(self) -> None:
        """Test tm.that() with wrong value."""
        data = {"key1": "value1"}
        expected = {"key1": "wrong_value"}
        with pytest.raises(
            AssertionError,
            match="expected 'wrong_value', got 'value1'",
        ):
            tm.that(data, kv=expected)

    def test_assert_list_contains_passes(self) -> None:
        """Test tm.that() with has parameter for list."""
        items = ["item1", "item2", "item3"]
        tm.that(items, has="item2")

    def test_assert_list_contains_missing_item(self) -> None:
        """Test tm.that() with item not in list."""
        items = ["item1", "item2"]
        with pytest.raises(AssertionError, match=r"Expected.*to contain 'item3'"):
            tm.that(items, has="item3")
