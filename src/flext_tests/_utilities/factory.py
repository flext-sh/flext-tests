"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import MutableMapping

from flext_tests import p, r, t


class FlextTestsFactoryUtilitiesMixin:
    """Factory helpers for test data creation."""

    @staticmethod
    def create_result[T](
        value: T | None = None,
        *,
        error: str | None = None,
    ) -> p.Result[T]:
        """Create r for tests.

        Args:
            value: Value for success result
            error: Error message for failure result

        Returns:
            r with value or error

        """
        if error is not None:
            return r[T].fail(error)
        if value is not None:
            return r[T].ok(value)
        return r[T].fail("No value or error provided")

    @staticmethod
    def create_test_data(
        **kwargs: t.Tests.TestobjectSerializable,
    ) -> MutableMapping[str, t.Tests.TestobjectSerializable]:
        """Create test data dictionary.

        Args:
            **kwargs: Key-value pairs for test data

        Returns:
            Configuration dictionary

        """
        return dict(kwargs)
