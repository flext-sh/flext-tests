"""Extracted mixin for flext_tests."""

from __future__ import annotations

from tests import p, t

from flext_tests import u


class FlextTestsContextHelpersUtilitiesMixin:
    """Helpers for context testing."""

    @staticmethod
    def assert_context_get_success(
        context: p.Context,
        key: str,
        expected_value: t.Tests.TestobjectSerializable,
    ) -> None:
        """Assert context get returns expected value.

        Args:
            context: p.Context instance
            key: Key to get
            expected_value: Expected value

        Raises:
            AssertionError: If value doesn't match

        """
        result = context.get(key)
        assert result.success, (
            f"Expected success for key '{key}', got: {result.error!r}"
        )
        raw_value = result.value
        actual = u.Tests.to_payload(raw_value)
        assert actual == expected_value, (
            f"Expected {expected_value!r} for key '{key}', got {result.value!r}"
        )
