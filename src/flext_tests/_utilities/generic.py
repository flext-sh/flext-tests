"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)

from flext_core import r
from flext_tests import t


class FlextTestsGenericHelpersUtilitiesMixin:
    """Generic helpers for test data creation."""

    @staticmethod
    def assert_result_chain[T](
        results: Sequence[r[T]],
        expected_successes: int | None = None,
        expected_failures: int | None = None,
        expected_success_count: int | None = None,
        expected_failure_count: int | None = None,
        first_failure_index: int | None = None,
    ) -> None:
        """Assert result chain has expected success/failure counts.

        Args:
            results: List of results to check
            expected_successes: Expected number of successes
            expected_failures: Expected number of failures
            expected_success_count: Alias for expected_successes
            expected_failure_count: Alias for expected_failures
            first_failure_index: Expected index of first failure (if any)

        Raises:
            AssertionError: If counts don't match

        """
        successes_expected = expected_successes or expected_success_count
        failures_expected = expected_failures or expected_failure_count
        successes = sum(1 for res in results if res.success)
        failures = sum(1 for res in results if res.failure)
        if successes_expected is not None:
            assert successes == successes_expected, (
                f"Expected {successes_expected} successes, got {successes}"
            )
        if failures_expected is not None:
            assert failures == failures_expected, (
                f"Expected {failures_expected} failures, got {failures}"
            )
        if first_failure_index is not None:
            actual_first_failure = next(
                (i for i, res in enumerate(results) if res.failure),
                None,
            )
            assert actual_first_failure == first_failure_index, (
                f"Expected first failure at index {first_failure_index}, got {actual_first_failure}"
            )
        elif failures == 0:
            actual_first_failure = next(
                (i for i, res in enumerate(results) if res.failure),
                None,
            )
            assert actual_first_failure is None, (
                f"Expected no failures but found first failure at index {actual_first_failure}"
            )

    @staticmethod
    def create_parametrized_cases(
        success_values: Sequence[t.Tests.TestobjectSerializable],
        failure_errors: t.StrSequence | None = None,
        *,
        error_codes: Sequence[str | None] | None = None,
    ) -> Sequence[
        tuple[
            r[t.Tests.TestobjectSerializable],
            bool,
            t.Tests.TestobjectSerializable | None,
            str | None,
        ]
    ]:
        """Create parametrized test cases from values and errors.

        Args:
            success_values: List of values for success results
            failure_errors: Optional list of error messages for failure results
            error_codes: Optional list of error codes for failure results

        Returns:
            r[TEntity]: Result containing created entity or error
            List of tuples (result, success, value, error)

        """
        cases: MutableSequence[
            tuple[
                r[t.Tests.TestobjectSerializable],
                bool,
                t.Tests.TestobjectSerializable | None,
                str | None,
            ]
        ] = []
        for value in success_values:
            result = r[t.Tests.TestobjectSerializable].ok(value)
            cases.append((result, True, value, None))
        if failure_errors:
            codes = error_codes or [None] * len(failure_errors)
            for i, error in enumerate(failure_errors):
                error_code = codes[i] if i < len(codes) else None
                result = r[t.Tests.TestobjectSerializable].fail(
                    error,
                    error_code=error_code,
                )
                cases.append((result, False, None, error))
        return cases

    @staticmethod
    def create_result_from_value[T](
        value: T | None,
        error_on_none: str = "Value cannot be None",
        default_on_none: T | None = None,
    ) -> r[T]:
        """Create result from value, failing if None (unless default).

        Args:
            value: Value to wrap in result
            error_on_none: Error message if value is None
            default_on_none: Default value to use if value is None

        Returns:
            r[TEntity]: Result containing created entity or error
            r with success or failure

        """
        if value is None:
            if default_on_none is not None:
                return r[T].ok(default_on_none)
            return r[T].fail(error_on_none)
        return r[T].ok(value)

    @staticmethod
    def validate_model_attributes(
        model: m.BaseModel,
        required_attrs: t.StrSequence,
        optional_attrs: t.StrSequence | None = None,
    ) -> r[bool]:
        """Validate model has required attributes.

        Args:
            model: Model t.NormalizedValue to validate
            required_attrs: List of required attribute names
            optional_attrs: Optional list of optional attribute names

        Returns:
            r[TEntity]: Result containing created entity or error
            r with True if all required attrs exist

        """
        _ = optional_attrs
        missing = [attr for attr in required_attrs if not hasattr(model, attr)]
        if missing:
            return r[bool].fail(f"Missing required attributes: {missing}")
        return r[bool].ok(value=True)
