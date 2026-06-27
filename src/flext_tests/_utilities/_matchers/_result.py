"""Result-oriented matcher helpers.

Exposes ``Tests.Matchers.check``, ``fail``, and ``ok`` for railway-result
assertions.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import TypeVar, overload

from flext_core import p as core_p
from flext_infra import u
from flext_tests import (
    FlextTestsMatchersAssertionsMixin,
    FlextTestsMatchersContainmentMixin,
    FlextTestsMatchersRulesMixin,
    FlextTestsMatchersTypeGuardsMixin,
    FlextTestsPayloadUtilities,
    FlextTestsResultUtilitiesMixin,
    c,
    m,
    p,
    t,
)

TResult = TypeVar("TResult")


class FlextTestsMatchersResultMixin:
    """Result assertion helpers exposed under ``Tests.Matchers``."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers:
            """Test matchers with powerful generalist methods."""

            @staticmethod
            def check(
                result: p.Result[TResult],
            ) -> m.Tests.Chain[TResult]:
                """Start chained assertions on result (railway pattern).

                Args:
                    result: Railway result to chain assertions on.

                Returns:
                    Chain t.JsonValue for fluent assertion API.

                """
                return m.Tests.Chain(result=result)

            @staticmethod
            def fail(
                result: p.Result[TResult],
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> str:
                r"""Enhanced assertion for r failure with optional error validation.

                Args:
                    result: r to check
                    error: Expected error substring (legacy parameter, use has=)
                    msg: Optional custom error message
                    has: Unified containment - error contains substring(s) (replaces contains)
                    lacks: Unified non-containment - error does NOT contain substring(s) (replaces excludes)
                    starts: Assert error starts with prefix
                    ends: Assert error ends with suffix
                    match: Assert error matches regex
                    code: Assert error code equals
                    code_has: Assert error code contains substring(s)
                    data: Assert error data contains key-value pairs
                    contains: Legacy parameter (deprecated, use has=)
                    excludes: Legacy parameter (deprecated, use lacks=)


                Returns:
                    Error message from result

                Raises:
                    AssertionError: If result is success or error doesn't satisfy constraints
                    ValueError: If parameter validation fails (via Pydantic model)

                """
                try:
                    params = m.Tests.FailParams.model_validate(kwargs)
                except c.EXC_BASIC_TYPE as exc:
                    raise ValueError(f"Parameter validation failed: {exc}") from exc
                err: str = FlextTestsResultUtilitiesMixin.assert_failure(result)
                if (
                    params.has
                    or params.lacks
                    or params.starts
                    or params.ends
                    or params.match
                ):
                    FlextTestsMatchersContainmentMixin._check_has_lacks(
                        err,
                        params.has,
                        params.lacks,
                        params.msg,
                        as_str=True,
                    )
                    if params.starts is not None and (
                        not u.chk(err, m.GuardCheckSpec(starts=params.starts))
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_NOT_STARTSWITH.format(
                                text=err,
                                prefix=params.starts,
                            ),
                        )
                    if params.ends is not None and (
                        not u.chk(err, m.GuardCheckSpec(ends=params.ends))
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_NOT_ENDSWITH.format(
                                text=err,
                                suffix=params.ends,
                            ),
                        )
                    if params.match is not None and params.match.search(err) is None:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_NOT_MATCHES.format(
                                text=err,
                                pattern=params.match.pattern,
                            ),
                        )
                if params.code is not None:
                    actual_code = result.error_code
                    if actual_code != params.code:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_ERROR_CODE_MISMATCH.format(
                                expected=params.code,
                                actual=actual_code,
                            ),
                        )
                if params.code_has is not None:
                    actual_code = result.error_code or ""
                    code_has_value = params.code_has
                    if isinstance(code_has_value, str):
                        items_list: t.StrSequence = [code_has_value]
                    else:
                        items_list = list(code_has_value)
                    for item in items_list:
                        if item not in actual_code:
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_ERROR_CODE_NOT_CONTAINS.format(
                                    expected=item,
                                    actual=actual_code,
                                ),
                            )
                if params.data is not None:
                    actual_raw = result.error_data
                    actual_data: MutableMapping[
                        str, t.Tests.TestobjectSerializable
                    ] = {}
                    if actual_raw is not None:
                        actual_data = {
                            k: FlextTestsPayloadUtilities.to_payload(v)
                            for k, v in actual_raw.items()
                        }
                    for key, expected_value in params.data.items():
                        if key not in actual_data:
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_ERROR_DATA_KEY_MISSING.format(
                                    key=key,
                                ),
                            )
                        if actual_data[key] != expected_value:
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_ERROR_DATA_VALUE_MISMATCH.format(
                                    key=key,
                                    expected=expected_value,
                                    actual=actual_data[key],
                                ),
                            )
                return err

            @staticmethod
            @overload
            def ok[TResult](result: core_p.Result[TResult]) -> TResult: ...

            @staticmethod
            @overload
            def ok[TResult](
                result: core_p.Result[TResult],
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> TResult | t.Tests.TestobjectSerializable: ...

            @staticmethod
            def ok[TResult](
                result: core_p.Result[TResult],
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> TResult | t.Tests.TestobjectSerializable:
                """Enhanced assertion for r success with optional value validation.

                Args:
                    result: Railway result expected to be success.
                    **kwargs: Validation criteria, validated by m.Tests.OkParams.

                Returns:
                    Unwrapped result value on success.

                Raises:
                    AssertionError: If result is failure or validation fails.

                """
                try:
                    params = m.Tests.OkParams.model_validate(kwargs)
                except c.EXC_BASIC_TYPE as exc:
                    raise ValueError(f"Parameter validation failed: {exc}") from exc
                result_value: TResult | t.Tests.TestobjectSerializable = (
                    FlextTestsResultUtilitiesMixin.assert_success(
                        result,
                        error_msg=params.msg,
                    )
                )
                extracted_payload: t.Tests.TestobjectSerializable | None = None
                if params.path is not None:
                    if isinstance(params.path, str):
                        path_str: str = params.path
                    else:
                        path_str = ".".join(params.path)
                    if not (isinstance(result_value, (m.BaseModel, Mapping))):
                        raise AssertionError(
                            params.msg
                            or f"Path extraction requires dict or model, got {type(result_value).__name__}",
                        )
                    try:
                        extract_data = FlextTestsPayloadUtilities.to_config_map(
                            result_value,
                        )
                    except c.ValidationError:
                        extract_data = m.ConfigMap(root={})
                    extracted = u.extract(extract_data, path_str)
                    if extracted.failure:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_SCOPE_PATH_NOT_FOUND.format(
                                path=path_str,
                                error=extracted.error,
                            ),
                        )
                    extracted_raw = extracted.value
                    extracted_payload = FlextTestsPayloadUtilities.to_payload(
                        extracted_raw,
                    )
                    result_value = extracted_payload
                has_validation = (
                    params.eq is not None
                    or params.ne is not None
                    or params.none is not None
                    or (params.empty is not None)
                    or (params.gt is not None)
                    or (params.gte is not None)
                    or (params.lt is not None)
                    or (params.lte is not None)
                    or (params.starts is not None)
                    or (params.ends is not None)
                    or (params.match is not None)
                )
                if has_validation:
                    is_type = params.is_ if not isinstance(params.is_, tuple) else None
                    result_payload = FlextTestsPayloadUtilities.to_payload(result_value)
                    eq_payload, ne_payload = (
                        FlextTestsMatchersTypeGuardsMixin.prepare_eq_ne_payloads(
                            result_payload,
                            params.eq,
                            params.ne,
                            msg=params.msg,
                            default_msg=(
                                f"Value {result_value!r} did not satisfy constraints"
                            ),
                        )
                    )
                    chk_value: t.GuardInput | None = (
                        None
                        if result_payload is None
                        else FlextTestsPayloadUtilities.to_normalized_value(
                            result_payload,
                        )
                    )
                    eq_plain = (
                        FlextTestsPayloadUtilities.to_normalized_value(eq_payload)
                        if eq_payload is not None
                        else None
                    )
                    ne_plain = (
                        FlextTestsPayloadUtilities.to_normalized_value(ne_payload)
                        if ne_payload is not None
                        else None
                    )
                    if not u.chk(
                        chk_value,
                        m.GuardCheckSpec.model_validate({
                            "eq": eq_plain,
                            "ne": ne_plain,
                            "is_": is_type,
                            "none": params.none,
                            "empty": params.empty,
                            "gt": params.gt,
                            "gte": params.gte,
                            "lt": params.lt,
                            "lte": params.lte,
                            "starts": params.starts,
                            "ends": params.ends,
                        }),
                    ):
                        error_msg = (
                            params.msg
                            or f"Value {result_value!r} did not satisfy constraints"
                        )
                        raise AssertionError(error_msg)
                    if (
                        params.match is not None
                        and isinstance(result_payload, str)
                        and params.match.search(result_payload) is None
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_NOT_MATCHES.format(
                                text=result_payload,
                                pattern=params.match.pattern,
                            ),
                        )
                if (
                    params.is_ is not None
                    and isinstance(params.is_, tuple)
                    and not any(
                        FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                            result_value,
                            expected_type,
                        )
                        for expected_type in params.is_
                    )
                ):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_TYPE_FAILED.format(
                            expected=params.is_,
                            actual=type(result_value).__name__,
                        ),
                    )
                FlextTestsMatchersContainmentMixin._check_has_lacks(
                    result_value,
                    params.has,
                    params.lacks,
                    params.msg,
                )
                result_payload = FlextTestsPayloadUtilities.to_payload(
                    result_value,
                )
                if params.len is not None:
                    FlextTestsMatchersAssertionsMixin.assert_len_match(
                        payload=result_payload,
                        sized=result_value,
                        length_spec=params.len,
                        msg=params.msg,
                    )
                if params.deep is not None:
                    if not isinstance(result_value, (m.BaseModel, Mapping)):
                        raise AssertionError(
                            params.msg
                            or f"Deep matching requires dict or model, got {type(result_value).__name__}",
                        )
                    deep_input: (
                        m.BaseModel | t.MappingKV[str, t.Tests.TestobjectSerializable]
                    )
                    if isinstance(result_value, m.BaseModel):
                        deep_input = result_value
                    else:
                        try:
                            deep_input = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                                result_value,
                            )
                        except c.ValidationError:
                            deep_input = {}
                    match_result = FlextTestsPayloadUtilities.deep_match(
                        deep_input, params.deep
                    )
                    if not match_result.matched:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_DEEP_PATH_FAILED.format(
                                path=match_result.path,
                                reason=match_result.reason,
                            ),
                        )
                if params.paths is not None:
                    FlextTestsMatchersRulesMixin._apply_path_rules(
                        result_payload,
                        params.paths,
                        inherited_msg=params.msg,
                    )
                if params.items is not None:
                    FlextTestsMatchersRulesMixin._apply_item_rules(
                        result_payload,
                        params.items,
                        inherited_msg=params.msg,
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersRulesMixin._apply_attribute_rules(
                        result.value,
                        params.attrs_match,
                        inherited_msg=params.msg,
                    )
                if params.path is None:
                    result_payload = FlextTestsPayloadUtilities.to_payload(
                        result.value,
                    )
                elif extracted_payload is not None:
                    result_payload = extracted_payload
                else:
                    result_payload = FlextTestsPayloadUtilities.to_payload(
                        result.value,
                    )
                if params.where is not None and (not params.where(result_payload)):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_PREDICATE_FAILED.format(
                            value=result_payload,
                        ),
                    )
                if result_value is None:
                    raise AssertionError(
                        params.msg
                        or "Value is None but validation passed - this should not happen",
                    )
                return result_payload


__all__: list[str] = ["FlextTestsMatchersResultMixin"]
