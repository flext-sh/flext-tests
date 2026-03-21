"""Unit tests for flext_tests.utilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import r
from pydantic import BaseModel, ConfigDict

from tests import u


class TestFlextTestsUtilitiesResult:
    """Test suite for u.Tests.Result class."""

    def test_assert_success_passes(self) -> None:
        """Test assert_success with successful result."""
        result = r[str].ok("success")
        value = u.Tests.Result.assert_success(result)
        u.Tests.Matchers.that(value == "success", eq=True)

    def test_assert_success_fails(self) -> None:
        """Test assert_success with failed result."""
        result: r[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            _ = u.Tests.Result.assert_success(result)

    def test_assert_failure_passes(self) -> None:
        """Test assert_failure with failed result."""
        result: r[str] = r[str].fail("error message")
        error = u.Tests.Result.assert_failure(result)
        u.Tests.Matchers.that(error == "error message", eq=True)

    def test_assert_failure_fails(self) -> None:
        """Test assert_failure with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            _ = u.Tests.Result.assert_failure(result)

    def test_assert_failure_with_expected_error(self) -> None:
        """Test assert_failure with expected error substring."""
        result: r[str] = r[str].fail("validation error occurred")
        error = u.Tests.Result.assert_failure(result, "validation")
        u.Tests.Matchers.that("validation" in error, eq=True)

    def test_assert_failure_with_expected_error_mismatch(self) -> None:
        """Test assert_failure when expected error doesn't match."""
        result: r[str] = r[str].fail("validation error occurred")
        with pytest.raises(AssertionError, match="Expected error containing"):
            _ = u.Tests.Result.assert_failure(result, "not found")

    def test_assert_success_with_value(self) -> None:
        """Test assert_success_with_value with matching value."""
        result = r[str].ok("expected")
        u.Tests.Result.assert_success_with_value(result, "expected")

    def test_assert_success_with_value_mismatch(self) -> None:
        """Test assert_success_with_value with non-matching value."""
        result = r[str].ok("actual")
        with pytest.raises(AssertionError):
            u.Tests.Result.assert_success_with_value(result, "expected")

    def test_assert_failure_with_error(self) -> None:
        """Test assert_failure_with_error with matching error."""
        result: r[str] = r[str].fail("test error")
        u.Tests.Result.assert_failure_with_error(result, "test")

    def test_assert_failure_with_error_mismatch(self) -> None:
        """Test assert_failure_with_error with non-matching error."""
        result: r[str] = r[str].fail("actual error")
        with pytest.raises(AssertionError):
            u.Tests.Result.assert_failure_with_error(result, "expected")


class TestFlextTestsUtilitiesTestContext:
    """Test suite for u.Tests.TestContext class."""

    def test_temporary_attribute_change(self) -> None:
        """Test temporary_attribute changes attribute temporarily."""

        class TestObject(BaseModel):
            attribute: str = "original"

        obj = TestObject()
        with u.Tests.TestContext.temporary_attribute(obj, "attribute", "modified"):
            u.Tests.Matchers.that(obj.attribute == "modified", eq=True)
        u.Tests.Matchers.that(obj.attribute == "original", eq=True)

    def test_temporary_attribute_new(self) -> None:
        """Test temporary_attribute adds new attribute temporarily."""

        class TestObject(BaseModel):
            model_config = ConfigDict(extra="allow")

        obj = TestObject()
        with u.Tests.TestContext.temporary_attribute(obj, "new_attr", "new_value"):
            u.Tests.Matchers.that(hasattr(obj, "new_attr"), eq=True)
            u.Tests.Matchers.that(
                getattr(obj, "new_attr", None) == "new_value", eq=True
            )
        u.Tests.Matchers.that(not hasattr(obj, "new_attr"), eq=True)

    def test_temporary_attribute_exception_restores(self) -> None:
        """Test temporary_attribute restores value even when exception occurs."""

        class TestObject(BaseModel):
            attribute: str = "original"

        obj = TestObject()
        with u.Tests.TestContext.temporary_attribute(obj, "attribute", "modified"):
            u.Tests.Matchers.that(obj.attribute == "modified", eq=True)
            msg = "Test exception"
            with pytest.raises(RuntimeError):
                raise RuntimeError(msg)
        u.Tests.Matchers.that(obj.attribute == "original", eq=True)


class TestFlextTestsUtilitiesFactory:
    """Test suite for u.Tests.Factory class."""

    def test_create_result_success(self) -> None:
        """Test create_result with value."""
        result = u.Tests.Factory.create_result("test_value")
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == "test_value", eq=True)

    def test_create_result_failure(self) -> None:
        """Test create_result with error."""
        result: r[str] = u.Tests.Factory.create_result(None, error="test error")
        u.Tests.Matchers.that(result.is_failure, eq=True)
        u.Tests.Matchers.that(result.error == "test error", eq=True)

    def test_create_result_no_args(self) -> None:
        """Test create_result with no arguments returns failure."""
        result: r[str] = u.Tests.Factory.create_result(None)
        u.Tests.Matchers.that(result.is_failure, eq=True)
        u.Tests.Matchers.that(result.error == "No value or error provided", eq=True)

    def test_create_test_data(self) -> None:
        """Test create_test_data creates dict with kwargs."""
        data = u.Tests.Factory.create_test_data(key1="value1", key2=42, key3=True)
        u.Tests.Matchers.that(data["key1"] == "value1", eq=True)
        u.Tests.Matchers.that(data["key2"] == 42, eq=True)
        u.Tests.Matchers.that(data["key3"] is True, eq=True)


class TestFlextTestsUtilitiesResultCompat:
    """Test suite for Result compatibility methods."""

    def test_assert_result_success_passes(self) -> None:
        """Test assert_result_success with successful result."""
        result = r[str].ok("success")
        _ = u.Tests.Result.assert_success(result)

    def test_assert_result_success_fails(self) -> None:
        """Test assert_result_success with failed result."""
        result: r[str] = r[str].fail("error")
        with pytest.raises(AssertionError, match="Expected success but got failure"):
            _ = u.Tests.Result.assert_success(result)

    def test_assert_result_failure_passes(self) -> None:
        """Test assert_result_failure with failed result."""
        result: r[str] = r[str].fail("error")
        _ = u.Tests.Result.assert_failure(result)

    def test_assert_result_failure_fails(self) -> None:
        """Test assert_result_failure with successful result."""
        result = r[str].ok("success")
        with pytest.raises(AssertionError, match="Expected failure but got success"):
            _ = u.Tests.Result.assert_failure(result)
