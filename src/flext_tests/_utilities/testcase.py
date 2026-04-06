"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
    MutableMapping,
    Sequence,
)

from flext_tests import (
    t,
)


class FlextTestsTestCaseHelpersUtilitiesMixin:
    """Helpers for creating test cases."""

    @staticmethod
    def create_batch_operation_test_cases(
        operation: str,
        descriptions: t.StrSequence,
        input_data_list: Sequence[Mapping[str, t.Tests.TestobjectSerializable]],
        expected_results: Sequence[t.Tests.TestobjectSerializable],
        **common_kwargs: t.Tests.TestobjectSerializable,
    ) -> Sequence[MutableMapping[str, t.Tests.TestobjectSerializable]]:
        """Create batch test cases for operation testing.

        Args:
            operation: Operation name
            descriptions: List of descriptions
            input_data_list: List of input data dicts
            expected_results: List of expected results
            **common_kwargs: Common parameters for all cases

        Returns:
            r[TEntity]: Result containing created entity or error
            List of test case dictionaries

        """
        th = FlextTestsTestCaseHelpersUtilitiesMixin
        cases: Sequence[MutableMapping[str, t.Tests.TestobjectSerializable]] = [
            th.create_operation_test_case(
                operation=operation,
                description=desc,
                input_data=data,
                expected_result=expected,
                **common_kwargs,
            )
            for desc, data, expected in zip(
                descriptions,
                input_data_list,
                expected_results,
                strict=True,
            )
        ]
        return cases

    @staticmethod
    def create_operation_test_case(
        operation: str,
        description: str,
        input_data: Mapping[str, t.Tests.TestobjectSerializable],
        expected_result: t.Tests.TestobjectSerializable,
        **kwargs: t.Tests.TestobjectSerializable,
    ) -> MutableMapping[str, t.Tests.TestobjectSerializable]:
        """Create a test case dict for operation testing.

        Args:
            operation: Operation name
            description: Test case description
            input_data: Input data for the operation
            expected_result: Expected result or type
            **kwargs: Additional test case parameters

        Returns:
            r[TEntity]: Result containing created entity or error
            Test case dictionary

        """
        result: MutableMapping[str, t.Tests.TestobjectSerializable] = {
            "operation": operation,
            "description": description,
            "input_data": input_data,
            "expected_result": expected_result,
        }
        result.update(kwargs)
        return result

    @staticmethod
    def execute_and_assert_operation_result(
        operation: Callable[[], t.Tests.TestobjectSerializable],
        test_case: Mapping[str, t.Tests.TestobjectSerializable],
    ) -> None:
        """Execute operation and assert result.

        Args:
            operation: Callable that returns the result
            test_case: Test case dict with expected_result

        Raises:
            AssertionError: If result doesn't match expectation

        """
        result = operation()
        expected = test_case.get("expected_result")
        assert result == expected, f"Expected {expected}, got {result}"
