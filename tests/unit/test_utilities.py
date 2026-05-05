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

    @pytest.mark.parametrize(
        ("result", "assertion", "expected"),
        [
            pytest.param(
                r[str].ok("success"),
                "success",
                "success",
                id="assert-success-pass",
            ),
            pytest.param(
                r[str].fail("error message"),
                "failure",
                "error message",
                id="assert-failure-pass",
            ),
        ],
    )
    def test_result_assertions_pass(
        self,
        result: p.Result[str],
        assertion: str,
        expected: str,
    ) -> None:
        """Successful result assertion helpers should return the unwrapped payload."""
        actual = (
            u.Tests.assert_success(result)
            if assertion == "success"
            else u.Tests.assert_failure(result)
        )
        tm.that(actual, eq=expected)

    @pytest.mark.parametrize(
        ("result", "assertion", "match"),
        [
            pytest.param(
                r[str].fail("error"),
                "success",
                "Expected success but got failure",
                id="assert-success-fail",
            ),
            pytest.param(
                r[str].ok("success"),
                "failure",
                "Expected failure but got success",
                id="assert-failure-fail",
            ),
        ],
    )
    def test_result_assertions_fail(
        self,
        result: p.Result[str],
        assertion: str,
        match: str,
    ) -> None:
        """Failing result assertion helpers should raise the expected assertion."""
        assertion_fn = (
            u.Tests.assert_success if assertion == "success" else u.Tests.assert_failure
        )
        with pytest.raises(AssertionError, match=match):
            _ = assertion_fn(result)

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

    def test_assert_result_chain_accepts_zero_alias_counts(self) -> None:
        """Explicit zero alias counts must not be treated as missing."""
        with pytest.raises(AssertionError, match="Expected 0 successes, got 1"):
            u.Tests.assert_result_chain(
                [r[str].ok("success")],
                expected_success_count=0,
            )

    def test_create_parametrized_cases_preserves_empty_error_codes(self) -> None:
        """Empty explicit error-code sequences must not be replaced by fallback data."""
        cases = u.Tests.create_parametrized_cases(
            success_values=(),
            failure_errors=("boom",),
            error_codes=(),
        )

        tm.that(len(cases), eq=1)
        tm.that(cases[0][0].error_code, eq=None)
