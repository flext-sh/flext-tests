"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
    MutableMapping,
)

from flext_cli import FlextCliUtilities
from flext_tests import (
    r,
    t,
)


class FlextTestsFactoryUtilitiesMixin:
    """Factory helpers for test data creation."""

    @staticmethod
    def add_operation(
        a: t.Tests.Testobject,
        b: t.Tests.Testobject,
    ) -> t.Tests.Testobject:
        """Execute add operation for numeric or string values.

        Args:
            a: First operand (numeric or string)
            b: Second operand (numeric or string)

        Returns:
            r[TEntity]: Result containing created entity or error
            Sum if both numeric, concatenation otherwise.

        """
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + b
        return str(a) + str(b)

    @staticmethod
    def create_error_operation(
        error_message: str,
    ) -> Callable[[], t.Tests.Testobject]:
        """Create callable that raises ValueError.

        Args:
            error_message: Error message for ValueError

        Returns:
            r[TEntity]: Result containing created entity or error
            Callable that raises ValueError when called.

        """

        def error_op() -> t.Tests.Testobject:
            raise ValueError(error_message)

        return error_op

    @staticmethod
    def create_result[T](
        value: T | None = None,
        *,
        error: str | None = None,
    ) -> r[T]:
        """Create r for tests.

        Args:
            value: Value for success result
            error: Error message for failure result

        Returns:
            r[TEntity]: Result containing created entity or error
            r with value or error

        """
        if error is not None:
            return r[T].fail(error)
        if value is not None:
            return r[T].ok(value)
        return r[T].fail("No value or error provided")

    @staticmethod
    def create_test_data(
        **kwargs: t.Tests.Testobject,
    ) -> MutableMapping[str, t.Tests.Testobject]:
        """Create test data dictionary.

        Args:
            **kwargs: Key-value pairs for test data

        Returns:
            r[TEntity]: Result containing created entity or error
            Configuration dictionary

        """
        return dict(kwargs)

    @staticmethod
    def execute_complex_service(
        validation_result: r[bool],
    ) -> r[t.Tests.Testobject]:
        """Execute complex service operation.

        Args:
            validation_result: Result of business rules validation

        Returns:
            r[TEntity]: Result containing created entity or error
            r with service data or error.

        """
        if validation_result.is_failure:
            return r[t.Tests.Testobject].fail(
                validation_result.error or "Validation failed",
            )
        result_data: t.Tests.Testobject = {"result": "success"}
        return r[t.Tests.Testobject].ok(result_data)

    @staticmethod
    def execute_default_service(service_type: str) -> r[t.Tests.Testobject]:
        """Execute default service operation.

        Args:
            service_type: Type of service

        Returns:
            r[TEntity]: Result containing created entity or error
            r with service type data.

        """
        service_data: t.Tests.Testobject = {"service_type": service_type}
        return r[t.Tests.Testobject].ok(service_data)

    @staticmethod
    def execute_user_service(
        overrides: Mapping[str, t.Tests.Testobject],
    ) -> r[t.Tests.Testobject]:
        """Execute user service operation.

        Args:
            overrides: Service configuration overrides

        Returns:
            r[TEntity]: Result containing created entity or error
            r with user data.

        """
        user_id = "default_123" if overrides.get("default") else "test_123"
        user_data: t.Tests.Testobject = {
            "user_id": user_id,
            "email": "test@example.com",
        }
        return r[t.Tests.Testobject].ok(user_data)

    @staticmethod
    def format_operation(name: str, value: int = 10) -> str:
        """Execute format operation returning formatted string.

        Args:
            name: Name part of format
            value: Value part of format (default: 10)

        Returns:
            r[TEntity]: Result containing created entity or error
            Formatted string "name: value".

        """
        return f"{name}: {value}"

    @staticmethod
    def generate_id() -> str:
        """Generate unique ID using FlextCliUtilities.generate().

        Returns:
            r[TEntity]: Result containing created entity or error
            Generated UUID string.

        """
        return FlextCliUtilities.generate()

    @staticmethod
    def generate_short_id(length: int = 8) -> str:
        """Generate short unique ID using FlextCliUtilities.generate('ulid', length=...).

        Args:
            length: Length of ID (default: 8)

        Returns:
            r[TEntity]: Result containing created entity or error
            Generated short ID string.

        """
        return FlextCliUtilities.generate("ulid", length=length)

    @staticmethod
    def simple_operation() -> t.Tests.Testobject:
        """Execute simple operation returning success message.

        Returns:
            r[TEntity]: Result containing created entity or error
            Success message string from constants.

        """
        return "success"
