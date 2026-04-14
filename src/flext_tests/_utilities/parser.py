"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
)

from flext_tests import p, t
from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin


class FlextTestsParserHelpersUtilitiesMixin:
    """Helpers for parser testing."""

    @staticmethod
    def execute_and_assert_parser_result[TResult: t.Tests.TestobjectSerializable](
        operation: Callable[[], p.Result[TResult]],
        expected_value: TResult | None = None,
        expected_error: str | None = None,
        description: str = "",
    ) -> None:
        """Execute parser operation and assert result.

        Args:
            operation: Callable that returns a r
            expected_value: Expected value on success
            expected_error: Expected error substring on failure
            description: Test case description for error messages

        """
        result: p.Result[TResult] = operation()
        if expected_error is not None:
            _ = FlextTestsResultUtilitiesMixin.assert_failure(result, expected_error)
            return
        value = FlextTestsResultUtilitiesMixin.assert_success(
            result,
            error_msg=(
                f"Expected success for: {description}, got: {result.error}"
                if description
                else None
            ),
        )
        if expected_value is not None and value != expected_value:
            msg = f"Want {expected_value}, got {value}: {description}"
            raise AssertionError(msg)
