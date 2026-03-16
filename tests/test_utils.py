"""Reusable test utilities for flext-tests.

Provides assertion helpers for testing FLEXT result types.
"""

from __future__ import annotations

from typing import TypeVar

from flext_core import r

T = TypeVar("T")


class AssertionHelpers:
    """Reusable assertion helpers to eliminate duplication."""

    @staticmethod
    def assert_flext_result_success[TResult](
        result: r[TResult],
        context: str = "",
        expected_type: type | None = None,
    ) -> TResult:
        """Assert r success with optional type checking."""
        assert result.is_success, f"{context}: Expected success, got: {result.error}"
        value = result.value
        if expected_type:
            assert isinstance(value, expected_type), (
                f"{context}: Expected {expected_type.__name__}, got {type(value).__name__}"
            )
        return value

    @staticmethod
    def assert_flext_result_failure[TResult](
        result: r[TResult],
        context: str = "",
        error_contains: str | None = None,
    ) -> str:
        """Assert r failure with optional error checking."""
        assert result.is_failure, (
            f"{context}: Expected failure, got success: {result.value}"
        )
        error_str = str(result.error)
        if error_contains:
            assert error_contains in error_str, (
                f"{context}: Expected error to contain '{error_contains}', got: {error_str}"
            )
        return error_str


assertion_helpers = AssertionHelpers()
