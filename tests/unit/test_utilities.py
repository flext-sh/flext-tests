"""Behavioral unit tests for the flext-tests utilities namespace (u.Tests).

Every test exercises only the PUBLIC contract of u.Tests helpers:
return values, r[T] outcomes, and the AssertionError / result-failure
semantics they promise. No private attribute access, no internal spying.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import r, tm
from tests import p, u


class TestsFlextTestsUtilities:
    """Behavioral contract for u.Tests result/data/make helpers."""

    # ------------------------------------------------------------------
    # assert_success / assert_failure — return values on the happy path
    # ------------------------------------------------------------------

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
        self, result: p.Result[str], assertion: str, expected: str
    ) -> None:
        """A matching assertion returns the success value / error string."""
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
        self, result: p.Result[str], assertion: str, match: str
    ) -> None:
        """A mismatched outcome raises AssertionError with a diagnostic message."""
        assertion_fn = (
            u.Tests.assert_success if assertion == "success" else u.Tests.assert_failure
        )
        with pytest.raises(AssertionError, match=match):
            _ = assertion_fn(result)

    def test_assert_failure_accepts_matching_error_substring(self) -> None:
        """A matching expected-error substring returns the full error text."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        error = u.Tests.assert_failure(result, "validation")
        tm.that(error, has="validation")

    def test_assert_failure_rejects_non_matching_error_substring(self) -> None:
        """A non-matching expected-error substring raises AssertionError."""
        result: p.Result[str] = r[str].fail("validation error occurred")
        with pytest.raises(AssertionError, match="Expected error containing"):
            _ = u.Tests.assert_failure(result, "not found")

    def test_assert_success_returns_value_when_expected_value_matches(self) -> None:
        """A matching expected_value passes and yields the unwrapped value."""
        result = r[str].ok("expected")
        returned = u.Tests.assert_success(result, expected_value="expected")
        tm.that(returned, eq="expected")

    def test_assert_success_rejects_non_matching_expected_value(self) -> None:
        """A non-matching expected_value raises AssertionError."""
        result = r[str].ok("actual")
        with pytest.raises(AssertionError, match="Expected success value"):
            _ = u.Tests.assert_success(result, expected_value="expected")

    # ------------------------------------------------------------------
    # assert_result_chain — count semantics
    # ------------------------------------------------------------------

    def test_assert_result_chain_passes_when_counts_match(self) -> None:
        """Matching success/failure counts and first-failure index pass silently."""
        chain: list[p.Result[str]] = [
            r[str].ok("a"),
            r[str].fail("boom"),
            r[str].ok("b"),
        ]
        # No AssertionError expected.
        u.Tests.assert_result_chain(
            chain, expected_successes=2, expected_failures=1, first_failure_index=1
        )

    def test_assert_result_chain_treats_zero_alias_count_as_explicit(self) -> None:
        """Explicit expected_success_count=0 is honored, not treated as unset."""
        with pytest.raises(AssertionError, match="Expected 0 successes, got 1"):
            u.Tests.assert_result_chain(
                [r[str].ok("success")], expected_success_count=0
            )

    def test_assert_result_chain_reports_wrong_first_failure_index(self) -> None:
        """A wrong first_failure_index raises AssertionError."""
        chain: list[p.Result[str]] = [r[str].ok("a"), r[str].fail("boom")]
        with pytest.raises(AssertionError, match="Expected first failure at index 0"):
            u.Tests.assert_result_chain(chain, first_failure_index=0)

    # ------------------------------------------------------------------
    # create_result_from_value — None handling contract
    # ------------------------------------------------------------------

    def test_create_result_from_value_wraps_present_value_as_success(self) -> None:
        """A non-None value yields a success result carrying that value."""
        result = u.Tests.create_result_from_value("payload")
        tm.that(u.Tests.assert_success(result), eq="payload")

    def test_create_result_from_value_fails_on_none_without_default(self) -> None:
        """None without a default yields a failure carrying the given message."""
        result = u.Tests.create_result_from_value(None, error_on_none="was none")
        error = u.Tests.assert_failure(result)
        tm.that(error, has="was none")

    def test_create_result_from_value_uses_default_on_none(self) -> None:
        """None with a default yields a success carrying the default."""
        result = u.Tests.create_result_from_value(None, default_on_none="fallback")
        tm.that(u.Tests.assert_success(result), eq="fallback")

    # ------------------------------------------------------------------
    # create_parametrized_cases — case-table generation contract
    # ------------------------------------------------------------------

    def test_create_parametrized_cases_builds_success_and_failure_rows(self) -> None:
        """Values and errors produce aligned (result, is_success, value, error) rows."""
        cases = u.Tests.create_parametrized_cases(
            success_values=("ok",), failure_errors=("boom",), error_codes=("E1",)
        )

        tm.that(len(cases), eq=2)
        success_row = cases[0]
        tm.that(u.Tests.assert_success(success_row[0]), eq="ok")
        tm.that(success_row[1], eq=True)
        tm.that(success_row[2], eq="ok")

        failure_row = cases[1]
        tm.that(u.Tests.assert_failure(failure_row[0]), has="boom")
        tm.that(failure_row[1], eq=False)
        tm.that(failure_row[3], eq="boom")
        tm.that(failure_row[0].error_code, eq="E1")

    def test_create_parametrized_cases_preserves_empty_error_codes(self) -> None:
        """An explicit empty error-code sequence leaves the failure code unset."""
        cases = u.Tests.create_parametrized_cases(
            success_values=(), failure_errors=("boom",), error_codes=()
        )

        tm.that(len(cases), eq=1)
        tm.that(cases[0][0].error_code, eq=None)

    # ------------------------------------------------------------------
    # make_has_executable_body — command-body detection contract
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        ("source", "expected_body"),
        [
            pytest.param(
                """#!/usr/bin/env python3
\"\"\"Header-only promoted command.\"\"\"
# /// flext-command
# verb = "demo"
# what = "all"
# ///

# comment-only trailer
""",
                False,
                id="header-only-has-no-executable-body",
            ),
            pytest.param(
                """#!/usr/bin/env python3
# /// flext-command
# verb = "demo"
# what = "body"
# ///

from __future__ import annotations
""",
                True,
                id="import-after-metadata-is-executable-body",
            ),
            pytest.param(
                """#!/usr/bin/env python3
SIDE_EFFECT = "detected"
# /// flext-command
# verb = "demo"
# what = "before"
# ///
""",
                True,
                id="assignment-before-metadata-is-executable-body",
            ),
        ],
    )
    def test_make_has_executable_body_classifies_command_source(
        self, tmp_path: Path, *, source: str, expected_body: bool
    ) -> None:
        """Executable statements outside the metadata header are detected."""
        script = tmp_path / "command.py"
        script.write_text(source, encoding="utf-8")

        result = u.Tests.make_has_executable_body(script)
        tm.that(u.Tests.assert_success(result), eq=expected_body)

    def test_make_has_executable_body_fails_for_missing_file(
        self, tmp_path: Path
    ) -> None:
        """A missing path yields a failure result rather than raising."""
        missing = tmp_path / "does_not_exist.py"
        result = u.Tests.make_has_executable_body(missing)
        error = u.Tests.assert_failure(result)
        tm.that(error, has="command body read")

    def test_make_has_executable_body_fails_for_invalid_python(
        self, tmp_path: Path
    ) -> None:
        """Unparseable Python yields a failure result naming the file."""
        broken = tmp_path / "broken.py"
        broken.write_text("def (:\n", encoding="utf-8")
        result = u.Tests.make_has_executable_body(broken)
        error = u.Tests.assert_failure(result)
        tm.that(error, has="broken.py")
