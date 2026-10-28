"""Result matcher utilities for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Callable, MutableMapping, Sequence
from typing import TypeAliasType, overload

from flext_tests import c, m, p, t
from flext_tests._utilities import FlextTestsUtilitiesPayload, FlextTestsUtilitiesResult
from flext_tests._utilities._matchers import FlextTestsUtilitiesMatchersThat


class FlextTestsUtilitiesMatchersResult:
    """Assertions over r[T] result values."""

    @classmethod
    def check[TResult](cls, result: p.Result[TResult]) -> m.Tests.Chain[TResult]:
        """Start chained assertions on result.

        Returns:
            The resulting ``m.Tests.Chain[TResult]``.

        """
        return m.Tests.Chain(result=result)

    @classmethod
    @overload
    def fail(cls, result: t.StrictBool, *, msg: str | None = None) -> bool: ...

    @classmethod
    @overload
    def fail(cls, result: p.ResultView[TResult], **kwargs: p.AttributeProbe) -> str: ...

    @classmethod
    def fail[TResult](
        cls,
        result: p.ResultView[TResult] | t.StrictBool,
        **kwargs: p.AttributeProbe,
    ) -> str | bool:
        """Require a false boolean or validate a failed result's error.

        Text criteria (``has``, ``lacks``, ``starts``, ``ends``, ``match``)
        are checked by ``that`` against the error string; ``code``,
        ``code_has`` and ``data`` are checked against the result.

        Returns:
            The unchanged false boolean or the result's error string.

        Raises:
            ValueError: If a boolean is combined with result-only criteria.

        """
        params = m.Tests.FailParams.model_validate(kwargs)
        that = FlextTestsUtilitiesMatchersThat.that
        if isinstance(result, bool):
            if params.model_fields_set - {"msg"}:
                msg = "Boolean failure checks accept only msg"
                raise ValueError(msg)
            that(result, eq=False, is_=bool, msg=params.msg)
            return result
        err: str = FlextTestsUtilitiesResult.assert_failure(result)
        if any(
            criterion is not None
            for criterion in (
                params.has,
                params.lacks,
                params.starts,
                params.ends,
                params.match,
            )
        ):
            that(
                err,
                has=params.has,
                lacks=params.lacks,
                starts=params.starts,
                ends=params.ends,
                match=params.match,
                msg=params.msg,
            )
        cls.fail_code(result, params)
        cls.fail_data(result, params)
        return err

    @classmethod
    def fail_code[TResult](
        cls,
        result: p.ResultView[TResult],
        params: m.Tests.FailParams,
    ) -> None:
        """Validate error code constraints.

        Raises:
            AssertionError: If ``params.code is not None and result.error_code
                != params.code``; or if ``item not in actual_code``.

        """
        if params.code is not None and result.error_code != params.code:
            raise AssertionError(
                params.msg
                or c.Tests.ERR_ERROR_CODE_MISMATCH.format(
                    expected=params.code,
                    actual=result.error_code,
                ),
            )
        if params.code_has is None:
            return
        actual_code = result.error_code or ""
        code_items: Sequence[str] = (
            [params.code_has]
            if isinstance(params.code_has, str)
            else list(params.code_has)
        )
        for item in code_items:
            if item not in actual_code:
                raise AssertionError(
                    params.msg
                    or c.Tests.ERR_ERROR_CODE_NOT_CONTAINS.format(
                        expected=item,
                        actual=actual_code,
                    ),
                )

    @classmethod
    def fail_data[TResult](
        cls,
        result: p.ResultView[TResult],
        params: m.Tests.FailParams,
    ) -> None:
        """Validate structured error data constraints.

        Raises:
            AssertionError: If ``key not in actual_data``; or if
                ``FlextTestsUtilitiesPayload.to_match_value(actual_data[key]) !=
                FlextTestsUtilitiesPayload.to_match_value(expected_value)``.

        """
        if params.data is None:
            return
        actual_raw = result.error_data
        actual_data: MutableMapping[str, p.Tests.Payload] = {}
        if actual_raw is not None:
            actual_data = {
                key: FlextTestsUtilitiesPayload.to_payload(
                    value,
                )
                for key, value in actual_raw.items()
            }
        for key, expected_value in params.data.items():
            if key not in actual_data:
                raise AssertionError(
                    params.msg or c.Tests.ERR_ERROR_DATA_KEY_MISSING.format(key=key),
                )
            if FlextTestsUtilitiesPayload.to_match_value(
                actual_data[key],
            ) != FlextTestsUtilitiesPayload.to_match_value(
                expected_value,
            ):
                raise AssertionError(
                    params.msg
                    or c.Tests.ERR_ERROR_DATA_VALUE_MISMATCH.format(
                        key=key,
                        expected=expected_value,
                        actual=actual_data[key],
                    ),
                )

    @classmethod
    @overload
    def ok(cls, result: t.StrictBool, *, msg: str | None = None) -> bool: ...

    @classmethod
    @overload
    def ok(
        cls,
        result: p.ResultView[TResult],
        *,
        path: None = None,
        eq: TResult
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        ne: TResult
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        where: Callable[[TResult], bool] | None = None,
        **kwargs: p.Tests.MatcherOption,
    ) -> TResult: ...

    @classmethod
    @overload
    def ok(
        cls,
        result: p.ResultView[TResult],
        *,
        path: t.Tests.PathSpec,
        eq: p.Tests.NativeMatchValue
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        ne: p.Tests.NativeMatchValue
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        where: Callable[[TResult], bool] | None = None,
        **kwargs: p.Tests.MatcherOption,
    ) -> p.Tests.NativeMatchValue: ...

    @classmethod
    def ok[TResult](
        cls,
        result: p.ResultView[TResult] | t.StrictBool,
        *,
        path: t.Tests.PathSpec | None = None,
        eq: TResult
        | p.Tests.NativeMatchValue
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        ne: TResult
        | p.Tests.NativeMatchValue
        | p.Tests.ApproxLike
        | TypeAliasType
        | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
        where: Callable[[TResult], bool] | None = None,
        **kwargs: p.Tests.MatcherOption,
    ) -> TResult | p.Tests.NativeMatchValue | bool:
        """Require a true boolean or validate a successful result's value.

        The success value, or the node selected by ``path``, is the subject
        every matcher criterion of ``that`` is applied to.

        Args:
            result: The result object to validate.
            path: The explicit path to select a value from the result.
            eq: The expected value for comparison.
            ne: The value that should not match the result.
            where: A callable predicate applied to the original success value.
            **kwargs: Additional matcher options.

        Returns:
            The validated result value or a native match value if applicable.

        Raises:
            AssertionError: If the `where` predicate fails or other validation
                checks fail.
            ValueError: If a boolean is combined with result-only criteria.

        """
        params = m.Tests.ThatParams.model_validate(kwargs)
        that = FlextTestsUtilitiesMatchersThat.that
        value_criteria = (
            eq is not c.Tests.MatcherMissing.OMITTED
            or ne is not c.Tests.MatcherMissing.OMITTED
            or bool(params.model_fields_set - {"msg"})
        )
        if isinstance(result, bool):
            if path is not None or where is not None or value_criteria:
                msg = "Boolean success checks accept only msg"
                raise ValueError(msg)
            that(result, eq=True, msg=params.msg)
            return result
        original = FlextTestsUtilitiesResult.assert_success(
            result,
            error_msg=params.msg,
        )
        if where is not None and not where(original):
            raise AssertionError(
                params.msg or c.Tests.ERR_PREDICATE_FAILED.format(value=original),
            )
        if path is None:
            if value_criteria:
                that(original, eq=eq, ne=ne, where=None, **kwargs)
            return original
        selected = FlextTestsUtilitiesPayload.to_match_value(
            FlextTestsUtilitiesPayload.extract_path_value(
                FlextTestsUtilitiesPayload.to_payload(original),
                path if isinstance(path, str) else ".".join(path),
            ),
        )
        if value_criteria:
            that(selected, eq=eq, ne=ne, where=None, **kwargs)
        return selected


__all__: list[str] = ["FlextTestsUtilitiesMatchersResult"]
