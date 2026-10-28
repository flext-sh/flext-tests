"""Behavioral unit tests for the flext-tests utilities namespace (u.Tests).

Every test exercises only the PUBLIC contract of u.Tests helpers:
return values, r[T] outcomes, and the AssertionError / result-failure
semantics they promise. No private attribute access, no internal spying.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests import p, r, tm, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsUtilities:
    """Behavioral contract for u.Tests result helpers and the file lock."""

    class Tests:
        """flext-tests utilities test namespace."""

    @staticmethod
    def test_file_lock_preserves_shared_inode_between_holders(
        tmp_path: Path,
    ) -> None:
        """Sequential holders coordinate through one persistent lock inode."""
        lock_path = tmp_path / "shared.lock"

        with u.Tests.FileLock(lock_path):
            first_inode = lock_path.stat().st_ino
        with u.Tests.FileLock(lock_path):
            second_inode = lock_path.stat().st_ino

        tm.that(second_inode, eq=first_inode)

    @staticmethod
    def test_file_lock_releases_after_body_failure(tmp_path: Path) -> None:
        """A failing holder releases its native lock for the next holder."""
        lock_path = tmp_path / "shared.lock"

        body_failure = ValueError("body failed")
        with (
            pytest.raises(ValueError, match=str(body_failure)),
            u.Tests.FileLock(lock_path),
        ):
            raise body_failure

        with u.Tests.FileLock(lock_path):
            tm.ok(lock_path.is_file())

    # ------------------------------------------------------------------
    # assert_success / assert_failure — return values on the happy path
    # ------------------------------------------------------------------

    @staticmethod
    @pytest.mark.parametrize(
        ("result", "assertion", "expected"),
        [
            pytest.param(
                r[str].ok("success"),
                "success",
                "success",
                id="assert-success-returns-payload",
            ),
            pytest.param(
                r[str].fail("error message"),
                "failure",
                "error message",
                id="assert-failure-returns-error",
            ),
        ],
    )
    def test_assertion_helper_returns_unwrapped_payload(
        result: p.Result[str],
        assertion: str,
        expected: str,
    ) -> None:
        """A matching assertion returns the success value / error string."""
        actual = (
            u.Tests.assert_success(result)
            if assertion == "success"
            else u.Tests.assert_failure(result)
        )
        tm.that(actual, eq=expected)

    @staticmethod
    @pytest.mark.parametrize(
        ("result", "assertion", "match"),
        [
            pytest.param(
                r[str].fail("error"),
                "success",
                "Expected success but got failure",
                id="assert-success-on-failure-raises",
            ),
            pytest.param(
                r[str].ok("success"),
                "failure",
                "Expected failure but got success",
                id="assert-failure-on-success-raises",
            ),
        ],
    )
    def test_assertion_helper_raises_on_mismatched_outcome(
        result: p.Result[str],
        assertion: str,
        match: str,
    ) -> None:
        """A mismatched outcome raises AssertionError with a diagnostic message."""
        assertion_fn = (
            u.Tests.assert_success if assertion == "success" else u.Tests.assert_failure
        )
        with pytest.raises(AssertionError, match=match):
            _ = assertion_fn(result)

    @staticmethod
    def test_assert_failure_accepts_matching_error_substring() -> None:
        """A matching expected-error substring returns the full error text."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        error = u.Tests.assert_failure(result, "validation")
        tm.that(error, has="validation")

    @staticmethod
    def test_assert_failure_rejects_non_matching_error_substring() -> None:
        """A non-matching expected-error substring raises AssertionError."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        with pytest.raises(AssertionError, match="Expected error containing"):
            _ = u.Tests.assert_failure(result, "not found")

    @staticmethod
    def test_assert_success_returns_value_when_expected_value_matches() -> None:
        """A matching expected_value passes and yields the unwrapped value."""
        result = r[str].ok("expected")
        returned = u.Tests.assert_success(result, expected_value="expected")
        tm.that(returned, eq="expected")

    @staticmethod
    def test_assert_success_rejects_non_matching_expected_value() -> None:
        """A non-matching expected_value raises AssertionError."""
        result = r[str].ok("actual")
        with pytest.raises(AssertionError, match="Expected success value"):
            _ = u.Tests.assert_success(result, expected_value="expected")
