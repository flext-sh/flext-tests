"""Extracted mixin for flext_tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests.constants import c

if TYPE_CHECKING:
    from types import EllipsisType

    from flext_tests.protocols import p


class FlextTestsResultUtilitiesMixin:
    """Result helpers for test assertions."""

    @staticmethod
    def assert_failure[TResult](
        result: p.Result[TResult],
        expected_error: str | None = None,
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
        return f"{error}"

    @staticmethod
    def assert_success[TResult](
        result: p.Result[TResult],
        error_msg: str | None = None,
        *,
        expected_value: TResult | EllipsisType = ...,
    ) -> TResult:
        """Assert result is success, optionally validate the value, and return it."""
        if not result.success:
            raise AssertionError(
                error_msg or c.Tests.ERR_OK_FAILED.format(error=result.error),
            )
        value: TResult = result.value
        if expected_value is not ... and value != expected_value:
            raise AssertionError(
                f"Expected success value {expected_value!r} but got {value!r}",
            )
        return value
