"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
)

from flext_tests import (
    r,
    t,
)


class FlextTestsParserHelpersUtilitiesMixin:
    """Helpers for parser testing."""

    @staticmethod
    def execute_and_assert_parser_result(
        operation: Callable[[], r[t.Tests.TestobjectSerializable]],
        expected_value: t.Tests.TestobjectSerializable | None = None,
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
        result = operation()
        if expected_error is not None:
            assert result.failure, f"Expected failure for: {description}, got success"
            m = f"'{expected_error}' not in '{result.error}': {description}"
            assert expected_error in str(result.error), m
        else:
            assert result.success, (
                f"Expected success for: {description}, got: {result.error}"
            )
            if expected_value is not None:
                m = f"Want {expected_value}, got {result.value}: {description}"
                assert result.value == expected_value, m
