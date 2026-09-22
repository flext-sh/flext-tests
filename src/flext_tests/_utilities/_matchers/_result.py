"""Result matcher utilities for flext-tests."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import cast, overload

from flext_core import p as core_p, u
from flext_tests import c, m, p, t

from ..payload import FlextTestsPayloadUtilities
from ..result import FlextTestsResultUtilitiesMixin
from ._assertions import FlextTestsMatchersAssertionsMixin
from ._containment import FlextTestsMatchersContainmentMixin
from ._that import FlextTestsMatchersThatMixin as FlextTestsMatchersRulesMixin
from ._typeguards import FlextTestsMatchersTypeGuardsMixin


class FlextTestsMatchersResultMixin:
    """Assertions over r[T] result values."""

    class Tests:
        """Test utility namespace."""

        class Matchers:
            """Matcher assertion helpers."""

            @staticmethod
            def check[TResult](result: p.Result[TResult]) -> m.Tests.Chain[TResult]:
                """Start chained assertions on result."""
                return m.Tests.Chain(result=result)

            @staticmethod
            def fail[TResult](
                result: core_p.ResultView[TResult], **kwargs: p.AttributeProbe
            ) -> str:
                """Assert that a result failed and validate its error payload."""
                params = m.Tests.FailParams.model_validate(kwargs)
                err: str = FlextTestsResultUtilitiesMixin.assert_failure(result)
                FlextTestsMatchersResultMixin.Tests.Matchers.fail_text(err, params)
                FlextTestsMatchersResultMixin.Tests.Matchers.fail_code(result, params)
                FlextTestsMatchersResultMixin.Tests.Matchers.fail_data(result, params)
                return err

            @staticmethod
            def fail_text(err: str, params: m.Tests.FailParams) -> None:
                """Validate textual error constraints."""
                if not any(
                    getattr(params, name)
                    for name in ("has", "lacks", "starts", "ends", "match")
                ):
                    return
                FlextTestsMatchersContainmentMixin.check_has_lacks(
                    err, params.has, params.lacks, params.msg, as_str=True
                )
                if params.starts is not None and (
                    not u.chk(err, m.GuardCheckSpec(starts=params.starts))
                ):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_NOT_STARTSWITH.format(
                            text=err, prefix=params.starts
                        )
                    )
                if params.ends is not None and (
                    not u.chk(err, m.GuardCheckSpec(ends=params.ends))
                ):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_NOT_ENDSWITH.format(text=err, suffix=params.ends)
                    )
                if params.match is not None and params.match.search(err) is None:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_NOT_MATCHES.format(
                            text=err, pattern=params.match.pattern
                        )
                    )

            @staticmethod
            def fail_code[TResult](
                result: core_p.ResultView[TResult], params: m.Tests.FailParams
            ) -> None:
                """Validate error code constraints."""
                if params.code is not None and result.error_code != params.code:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ERROR_CODE_MISMATCH.format(
                            expected=params.code, actual=result.error_code
                        )
                    )
                if params.code_has is None:
                    return
                actual_code = result.error_code or ""
                code_items: t.StrSequence = (
                    [params.code_has]
                    if isinstance(params.code_has, str)
                    else list(params.code_has)
                )
                for item in code_items:
                    if item not in actual_code:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_ERROR_CODE_NOT_CONTAINS.format(
                                expected=item, actual=actual_code
                            )
                        )

            @staticmethod
            def fail_data[TResult](
                result: core_p.ResultView[TResult], params: m.Tests.FailParams
            ) -> None:
                """Validate structured error data constraints."""
                if params.data is None:
                    return
                actual_raw = result.error_data
                actual_data: MutableMapping[str, p.Tests.Payload] = {}
                if actual_raw is not None:
                    actual_data = {
                        key: FlextTestsPayloadUtilities.to_payload(value)
                        for key, value in actual_raw.items()
                    }
                for key, expected_value in params.data.items():
                    if key not in actual_data:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_ERROR_DATA_KEY_MISSING.format(key=key)
                        )
                    if FlextTestsPayloadUtilities.to_match_value(
                        actual_data[key]
                    ) != FlextTestsPayloadUtilities.to_match_value(expected_value):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_ERROR_DATA_VALUE_MISMATCH.format(
                                key=key,
                                expected=expected_value,
                                actual=actual_data[key],
                            )
                        )

            @staticmethod
            def ok_extract_path[TResult](
                result_value: TResult, params: m.Tests.OkParams
            ) -> tuple[TResult | p.Tests.Payload, p.Tests.Payload | None]:
                """Extract an owned node without dumping native model leaves."""
                if params.path is None:
                    return result_value, None
                path = (
                    params.path
                    if isinstance(params.path, str)
                    else ".".join(params.path)
                )
                payload = FlextTestsMatchersRulesMixin.extract_path_value(
                    FlextTestsPayloadUtilities.to_payload(result_value), path
                )
                return payload, payload

            @staticmethod
            def ok_has_scalar_validation(params: m.Tests.OkParams) -> bool:
                """Return whether scalar guard validation is requested."""
                return any(
                    getattr(params, name) is not None
                    for name in (
                        "eq",
                        "ne",
                        "none",
                        "empty",
                        "gt",
                        "gte",
                        "lt",
                        "lte",
                        "starts",
                        "ends",
                        "match",
                    )
                )

            @staticmethod
            def ok_preserves_result_identity(params: m.Tests.OkParams) -> bool:
                """True when no structural extraction kwargs are set (return TResult)."""
                return all(
                    getattr(params, name) is None
                    for name in (
                        "path",
                        "len",
                        "deep",
                        "paths",
                        "items",
                        "attrs_match",
                        "where",
                    )
                )

            @staticmethod
            def ok_validate_scalar[TResult](
                result_value: TResult, params: m.Tests.OkParams
            ) -> TResult:
                """Validate native equality and finite scalar constraints."""
                if FlextTestsMatchersResultMixin.Tests.Matchers.ok_has_scalar_validation(
                    params
                ):
                    FlextTestsMatchersTypeGuardsMixin.assert_scalar_match(
                        FlextTestsPayloadUtilities.to_payload(result_value), params
                    )
                return result_value

            @staticmethod
            def ok_validate_type[TResult](
                result_value: TResult, params: m.Tests.OkParams
            ) -> TResult:
                """Check the original successful value's declared runtime types."""
                if params.is_ is not None:
                    native = (
                        FlextTestsPayloadUtilities.to_match_value(result_value)
                        if isinstance(result_value, m.Tests.Payload)
                        else result_value
                    )
                    if not FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                        native, params.is_
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_TYPE_FAILED.format(
                                expected=params.is_, actual=type(native).__name__
                            )
                        )
                return result_value

            @staticmethod
            @overload
            def ok[TResult](result: core_p.ResultView[TResult]) -> TResult: ...

            @staticmethod
            @overload
            def ok[TResult](
                result: core_p.ResultView[TResult], **kwargs: p.AttributeProbe
            ) -> TResult | t.Tests.NativeMatchValue: ...

            @staticmethod
            def ok[TResult](
                result: core_p.ResultView[TResult], **kwargs: p.AttributeProbe
            ) -> TResult | t.Tests.NativeMatchValue:
                # mro-j47u: matchers observe the protocol and preserve source identity.
                if not kwargs:
                    return FlextTestsResultUtilitiesMixin.assert_success(result)
                params = m.Tests.OkParams.model_validate(kwargs)
                result_value: TResult | p.Tests.Payload = (
                    FlextTestsResultUtilitiesMixin.assert_success(
                        result, error_msg=params.msg
                    )
                )
                result_value, extracted_payload = (
                    FlextTestsMatchersResultMixin.Tests.Matchers.ok_extract_path(
                        result_value, params
                    )
                )
                result_value = (
                    FlextTestsMatchersResultMixin.Tests.Matchers.ok_validate_scalar(
                        result_value, params
                    )
                )
                result_value = (
                    FlextTestsMatchersResultMixin.Tests.Matchers.ok_validate_type(
                        result_value, params
                    )
                )
                if params.has is not None or params.lacks is not None:
                    FlextTestsMatchersContainmentMixin.check_has_lacks(
                        result_value, params.has, params.lacks, params.msg
                    )
                if FlextTestsMatchersResultMixin.Tests.Matchers.ok_preserves_result_identity(
                    params
                ):
                    # No structural extraction was requested, so ok_extract_path
                    # returned the success value unchanged; the subject keeps its
                    # TResult identity across the scalar/type validators.
                    return cast("TResult", result_value)
                result_payload = (
                    FlextTestsMatchersResultMixin.Tests.Matchers.ok_payload(
                        result, result_value, extracted_payload, params
                    )
                )
                FlextTestsMatchersResultMixin.Tests.Matchers.ok_validate_structured(
                    result, result_value, result_payload, params
                )
                return FlextTestsPayloadUtilities.to_match_value(result_payload)

            @staticmethod
            def ok_payload[TResult](
                result: core_p.ResultView[TResult],
                result_value: TResult | p.Tests.Payload,
                extracted_payload: p.Tests.Payload | None,
                params: m.Tests.OkParams,
            ) -> p.Tests.Payload:
                if params.path is None:
                    return FlextTestsPayloadUtilities.to_payload(result.value)
                if extracted_payload is not None:
                    return extracted_payload
                return FlextTestsPayloadUtilities.to_payload(result_value)

            @staticmethod
            def ok_validate_structured[TResult](
                result: core_p.ResultView[TResult],
                result_value: TResult | p.Tests.Payload,
                result_payload: p.Tests.Payload,
                params: m.Tests.OkParams,
            ) -> None:
                if params.len is not None:
                    FlextTestsMatchersAssertionsMixin.assert_len_match(
                        payload=result_payload,
                        sized=result_value,
                        length_spec=params.len,
                        msg=params.msg,
                    )
                if params.deep is not None:
                    FlextTestsMatchersResultMixin.Tests.Matchers.ok_validate_deep(
                        result_value, params
                    )
                if params.paths is not None:
                    FlextTestsMatchersRulesMixin.apply_path_rules(
                        result_payload, params.paths, inherited_msg=params.msg
                    )
                if params.items is not None:
                    FlextTestsMatchersRulesMixin.apply_item_rules(
                        result_payload, params.items, inherited_msg=params.msg
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersRulesMixin.apply_attribute_rules(
                        result.value, params.attrs_match, inherited_msg=params.msg
                    )
                if params.where is not None and (not params.where(result_payload)):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_PREDICATE_FAILED.format(value=result_payload)
                    )

            @staticmethod
            def ok_validate_deep[TResult](
                result_value: TResult, params: m.Tests.OkParams
            ) -> TResult:
                """Deep matching reads the canonical owned payload tree."""
                if params.deep is None:
                    return result_value
                match_result = FlextTestsPayloadUtilities.deep_match(
                    FlextTestsPayloadUtilities.to_payload(result_value), params.deep
                )
                if not match_result.matched:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_DEEP_PATH_FAILED.format(
                            path=match_result.path, reason=match_result.reason
                        )
                    )
                return result_value


__all__: list[str] = ["FlextTestsMatchersResultMixin"]
