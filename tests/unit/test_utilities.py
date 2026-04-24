"""Unit tests for flext_tests.utilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

import pytest

from flext_tests import tm
from tests import m, p, r, u


class TestsFlextTestsUtilitiesUnit:
    """Test suite for u.Tests.Result class."""

    def test_assert_success_passes(self) -> None:
        """Test assert_success with successful result."""
        result = r[str].ok("success")
        value = u.Tests.assert_success(result)
        tm.that(value, eq="success")

    def test_assert_success_fails(self) -> None:
        """Test assert_success with failed result."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            _ = u.Tests.assert_success(result)

    def test_assert_failure_passes(self) -> None:
        """Test assert_failure with failed result."""
        result: p.Result[str] = r[str].fail("error message")
        error = u.Tests.assert_failure(result)
        tm.that(error, eq="error message")

    def test_assert_failure_fails(self) -> None:
        """Test assert_failure with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            _ = u.Tests.assert_failure(result)

    def test_assert_failure_with_expected_error(self) -> None:
        """Test assert_failure with expected error substring."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        error = u.Tests.assert_failure(result, "validation")
        tm.that(error, has="validation")

    def test_assert_failure_with_expected_error_mismatch(self) -> None:
        """Test assert_failure when expected error doesn't match."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        with pytest.raises(AssertionError, match="Expected error containing"):
            _ = u.Tests.assert_failure(result, "not found")

    def test_assert_success_with_value(self) -> None:
        """Test assert_success_with_value with matching value."""
        result = r[str].ok("expected")
        u.Tests.assert_success_with_value(result, "expected")

    def test_assert_success_with_value_mismatch(self) -> None:
        """Test assert_success_with_value with non-matching value."""
        result = r[str].ok("actual")
        with pytest.raises(AssertionError):
            u.Tests.assert_success_with_value(result, "expected")

    def test_assert_failure_with_error(self) -> None:
        """Test assert_failure_with_error with matching error."""
        result: p.Result[str] = r[str].fail("test error")
        u.Tests.assert_failure_with_error(result, "test")

    def test_assert_failure_with_error_mismatch(self) -> None:
        """Test assert_failure_with_error with non-matching error."""
        result: p.Result[str] = r[str].fail("actual error")
        with pytest.raises(AssertionError):
            u.Tests.assert_failure_with_error(result, "expected")

    def test_temporary_attribute_change(self) -> None:
        """Test temporary_attribute changes attribute temporarily."""

        class TestObject(m.BaseModel):
            attribute: str = "original"

        obj = TestObject()
        with u.Tests.temporary_attribute(obj, "attribute", "modified"):
            tm.that(obj.attribute, eq="modified")
        tm.that(obj.attribute, eq="original")

    def test_temporary_attribute_new(self) -> None:
        """Test temporary_attribute adds new attribute temporarily."""

        class TestObject(m.BaseModel):
            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="allow")

        obj = TestObject()
        with u.Tests.temporary_attribute(obj, "new_attr", "new_value"):
            pass
        tm.that(not hasattr(obj, "new_attr"), eq=True)

    def test_temporary_attribute_exception_restores(self) -> None:
        """Test temporary_attribute restores value even when exception occurs."""

        class TestObject(m.BaseModel):
            attribute: str = "original"

        obj = TestObject()
        with u.Tests.temporary_attribute(obj, "attribute", "modified"):
            tm.that(obj.attribute, eq="modified")
            msg = "Test exception"
            with pytest.raises(RuntimeError):
                raise RuntimeError(msg)
        tm.that(obj.attribute, eq="original")

    def test_assert_result_success_passes(self) -> None:
        """Test assert_result_success with successful result."""
        result = r[str].ok("success")
        _ = u.Tests.assert_success(result)

    def test_assert_result_success_fails(self) -> None:
        """Test assert_result_success with failed result."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            _ = u.Tests.assert_success(result)

    def test_assert_result_failure_passes(self) -> None:
        """Test assert_result_failure with failed result."""
        result: p.Result[str] = r[str].fail("error")
        _ = u.Tests.assert_failure(result)

    def test_assert_result_failure_fails(self) -> None:
        """Test assert_result_failure with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            _ = u.Tests.assert_failure(result)

    def test_execute_and_assert_parser_result_success(self) -> None:
        """Helper should pass when parser operation returns expected success value."""

        def operation() -> p.Result[str]:
            return r[str].ok("parsed")

        u.Tests.execute_and_assert_parser_result(
            operation,
            expected_value="parsed",
            description="parser success",
        )

    def test_execute_and_assert_parser_result_failure(self) -> None:
        """Helper should pass when parser operation returns expected failure."""

        def operation() -> p.Result[str]:
            return r[str].fail("invalid input")

        u.Tests.execute_and_assert_parser_result(
            operation,
            expected_error="invalid",
            description="parser failure",
        )

    def test_execute_and_assert_parser_result_value_mismatch(self) -> None:
        """Helper should raise when success value differs from expected."""

        def operation() -> p.Result[str]:
            return r[str].ok("actual")

        with pytest.raises(AssertionError):
            u.Tests.execute_and_assert_parser_result(
                operation,
                expected_value="expected",
                description="value mismatch",
            )
