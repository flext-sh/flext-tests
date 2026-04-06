"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_tests import (
    t,
)


class FlextTestsAssertionsUtilitiesMixin:
    """Common assertion helpers."""

    @staticmethod
    def assert_result_matches_expected(
        result: t.Tests.Testobject,
        expected_type: type,
        description: str = "",
    ) -> None:
        """Assert result is instance of expected type.

        Args:
            result: Value to check
            expected_type: Expected type
            description: Optional test description for error messages

        Raises:
            AssertionError: If result is not instance of expected_type

        """
        assert isinstance(result, expected_type), (
            f"Expected {expected_type.__name__}, got {type(result).__name__}{(f' for {description}' if description else '')}"
        )
