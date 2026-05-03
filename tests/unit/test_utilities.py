"""Unit tests for flext_tests.utilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_tests import tm
from tests import p, r, u


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

    def test_assert_success_with_expected_value(self) -> None:
        """Test assert_success with matching expected_value."""
        result = r[str].ok("expected")
        u.Tests.assert_success(result, expected_value="expected")

    def test_assert_success_with_expected_value_mismatch(self) -> None:
        """Test assert_success when expected_value does not match."""
        result = r[str].ok("actual")
        with pytest.raises(AssertionError, match="Expected success value"):
            u.Tests.assert_success(result, expected_value="expected")

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
