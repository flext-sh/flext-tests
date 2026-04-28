"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_core import FlextProtocolsResult
from flext_tests import p


class FlextTestsResultUtilitiesMixin:
    """Result helpers for test assertions."""

    @staticmethod
    def assert_failure[TResult](
        result: p.Result[TResult], expected_error: str | None = None
    ) -> str:
        """Assert result is failure and return error message."""
        if result.success:
            msg = f"Expected failure but got success: {result.value}"
            raise AssertionError(msg)
        error = result.error
        if error is None:
            msg = "Expected error but got None"
            raise AssertionError(msg)
        if expected_error and expected_error not in error:
            msg = f"Expected error containing '{expected_error}' but got: {error}"
            raise AssertionError(msg)
        return str(error)

    @staticmethod
    def assert_failure_with_error[T](
        result: p.Result[T], expected_error: str | None = None
    ) -> None:
        """Assert result is failure and has expected error.

        Args:
            result: r or Result protocol to check
            expected_error: Optional expected error substring

        Raises:
            AssertionError: If result is success or error doesn't match

        """
        if result.success:
            msg = f"Expected failure, got success: {result.value}"
            raise AssertionError(msg)
        if expected_error:
            assert result.error is not None
            assert expected_error in result.error

    @staticmethod
    def assert_success[TResult](
        result: FlextProtocolsResult.Result[TResult], error_msg: str | None = None
    ) -> TResult:
        """Assert result is success and return unwrapped value."""
        if not result.success:
            msg = error_msg or f"Expected success but got failure: {result.error}"
            raise AssertionError(msg)
        value: TResult = result.value
        return value

    @staticmethod
    def assert_success_with_value[TResult](
        result: p.Result[TResult],
        expected_value: TResult,
    ) -> None:
        """Assert result is success and has expected value."""
        if not result.success:
            msg = f"Expected success, got failure: {result.error}"
            raise AssertionError(msg)
        assert result.value == expected_value
