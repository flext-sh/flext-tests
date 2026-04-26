"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with powerful generalist methods.
Short alias: tm (test matchers)

Core Philosophy:
- MINIMAL API: Only 5 core methods (ok, fail, check, that, scope)
- POWERFUL: Each method handles multiple scenarios via optional parameters
- UNIVERSAL: tm.that() does ALL validations (equality, type, length, containment, etc.)

Core Methods (5 main methods):
    tm.ok(result, **kw)     # Assert r success, optional validation
    tm.fail(result, **kw)   # Assert r failure, optional validation
    tm.check(result)        # Railway-pattern chained assertions
    tm.that(value, **kw)    # Universal assertion - ALL validations in ONE method
    tm.scope()              # Isolated test context (context manager)

Usage Examples:
    # r assertions
    value = tm.ok(result)                    # Assert success, return value
    tm.ok(result, eq="expected")            # Assert success and equals
    tm.fail(result, contains="error")       # Assert failure with error check

    # Universal assertions (tm.that() does EVERYTHING)
    tm.that(x, gt=0, lt=100)                 # Comparisons
    tm.that(v, is_=str, none=False)          # Type and None
    tm.that(d, contains="key")               # Containment (dict/list/str)
    tm.that(lst, length=5, length_gt=0)      # Length checks
    tm.that(text, starts="http", ends="/")   # String validation
    tm.that(text, match="[0-9]{4}-[0-9]{2}")    # Regex match

    # Chained assertions
    tm.check(result).ok().eq(5).done()       # Railway pattern

Deprecated Methods (use tm.that() instead):
    tm.that() -> tm.that(actual, eq=eq=expected)
    tm.true() -> tm.that(condition, eq=True)
    tm.assert_contains() -> tm.that(container, contains=item)
    tm.str_() -> tm.that(text, contains/starts/ends/match/excludes/empty=...)
    tm.is_() -> tm.that(value, is_=type, none=...)
    tm.len() -> tm.that(items, length/length_gt/length_gte/empty=...)
    tm.hasattr() -> tm.that(hasattr(obj, attr), eq=True)
    tm.method() -> tm.that(hasattr(...), eq=True) + tm.that(callable(...), eq=True)
    tm.not_none() -> tm.that(value, none=False)

Note: For test data creation, use tb() (FlextTestsBuilders) instead:
    data = tb().with_users(10).with_configs(production=True).build()

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import warnings
from collections.abc import (
    Generator,
    Mapping,
    MutableMapping,
    Sequence,
    Sized,
)
from contextlib import contextmanager, nullcontext
from datetime import datetime
from pathlib import Path
from typing import Never, TypeIs, overload

from flext_core import FlextProtocolsResult, u
from flext_tests import (
    FlextTestsConfigHelpersUtilitiesMixin,
    FlextTestsPayloadUtilities,
    c,
    m,
    p,
    t,
)


class FlextTestsMatchersUtilities:
    """Namespace for test matcher utilities used in flext-tests."""

    _GUARD_EQ_TYPES: tuple[type, ...] = (
        str,
        int,
        float,
        bool,
        bytes,
        datetime,
        Path,
    )

    @staticmethod
    def _matches_runtime_type(
        value: object,
        expected_type: type | tuple[type, ...],
    ) -> bool:
        """Check runtime type compatibility using flext-core guards."""
        if isinstance(expected_type, tuple):
            return any(
                FlextTestsMatchersUtilities._matches_runtime_type(value, item)
                for item in expected_type
            )
        return u.instance_of(value, expected_type)

    @staticmethod
    def _supports_guard_eq(
        value: t.Tests.TestobjectSerializable | None,
    ) -> bool:
        return value is None or isinstance(
            value,
            FlextTestsMatchersUtilities._GUARD_EQ_TYPES,
        )

    @staticmethod
    def _prepare_eq_ne_payloads(
        actual_payload: t.Tests.TestobjectSerializable,
        eq_value: t.Tests.MatcherKwargValue | t.Tests.TestobjectSerializable | None,
        ne_value: t.Tests.MatcherKwargValue | t.Tests.TestobjectSerializable | None,
        *,
        msg: str | None,
        default_msg: str,
    ) -> tuple[
        t.Tests.TestobjectSerializable | None,
        t.Tests.TestobjectSerializable | None,
    ]:
        eq_payload = (
            FlextTestsPayloadUtilities.to_payload(eq_value)
            if eq_value is not None
            else None
        )
        ne_payload = (
            FlextTestsPayloadUtilities.to_payload(ne_value)
            if ne_value is not None
            else None
        )
        if (
            eq_payload is not None
            and not FlextTestsMatchersUtilities._supports_guard_eq(
                eq_payload,
            )
        ):
            if actual_payload != eq_payload:
                raise AssertionError(msg or default_msg)
            eq_payload = None
        if (
            ne_payload is not None
            and not FlextTestsMatchersUtilities._supports_guard_eq(
                ne_payload,
            )
        ):
            if actual_payload == ne_payload:
                raise AssertionError(msg or default_msg)
            ne_payload = None
        return (eq_payload, ne_payload)

    @staticmethod
    def _raise_match_assertion(
        template: str,
        *,
        msg: str | None,
        container: object,
        item: object,
    ) -> Never:
        """Raise AssertionError with ``msg`` or formatted ``template``."""
        raise AssertionError(
            msg or template.format(container=container, item=item),
        )

    @staticmethod
    def _assert_len_match(
        *,
        payload: t.Tests.TestobjectSerializable,
        sized: object,
        length_spec: int | tuple[int, int],
        msg: str | None,
    ) -> None:
        """Raise AssertionError if ``payload`` length doesn't match ``length_spec``."""
        if FlextTestsPayloadUtilities.length_validate(payload, length_spec):
            return
        actual_len = len(sized) if isinstance(sized, Sized) else 0
        if isinstance(length_spec, int):
            raise AssertionError(
                msg
                or c.Tests.ERR_LEN_EXACT_FAILED.format(
                    expected=length_spec,
                    actual=actual_len,
                ),
            )
        raise AssertionError(
            msg
            or c.Tests.ERR_LEN_RANGE_FAILED.format(
                min=length_spec[0],
                max=length_spec[1],
                actual=actual_len,
            ),
        )

    @staticmethod
    def _rule_to_kwargs(
        rule: t.Tests.MatchRuleSpec,
        *,
        inherited_msg: str | None = None,
    ) -> dict[str, t.Tests.MatcherKwargValue]:
        """Normalize one declarative matcher rule into tm.that()-compatible kwargs."""
        kwargs_t = dict[str, t.Tests.MatcherKwargValue]
        if isinstance(rule, Mapping):
            raw_mapping = {str(key): value for key, value in rule.items()}
            if raw_mapping and set(raw_mapping).issubset(
                c.Tests.MATCHER_RULE_KEYS,
            ):
                normalized_mapping = dict(raw_mapping)
                if inherited_msg is not None and "msg" not in normalized_mapping:
                    normalized_mapping["msg"] = inherited_msg
                return normalized_mapping
            eq_value: t.Tests.Testobject = FlextTestsPayloadUtilities.to_payload(rule)
            result: kwargs_t = {"eq": eq_value}
            if inherited_msg:
                result["msg"] = inherited_msg
            return result
        if isinstance(rule, type):
            return (
                {"is_": rule, "msg": inherited_msg} if inherited_msg else {"is_": rule}
            )
        if isinstance(rule, tuple) and all(isinstance(item, type) for item in rule):
            return (
                {"is_": rule, "msg": inherited_msg} if inherited_msg else {"is_": rule}
            )
        if callable(rule):
            return (
                {"where": rule, "msg": inherited_msg}
                if inherited_msg
                else {"where": rule}
            )
        fallback: kwargs_t = {"eq": rule}
        if inherited_msg:
            fallback["msg"] = inherited_msg
        return fallback

    @staticmethod
    def _extract_mapping_path(
        value: t.Tests.TestobjectSerializable
        | m.BaseModel
        | Mapping[str, t.Tests.TestobjectSerializable],
        path: str,
    ) -> t.Tests.TestobjectSerializable:
        """Extract one dotted path from a model or mapping using flext-core extract helpers."""
        extract_source: m.ConfigMap
        if isinstance(value, m.BaseModel):
            extract_source = m.ConfigMap.model_validate({
                str(key): FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(item),
                )
                for key, item in value.model_dump(mode="python").items()
            })
        elif isinstance(value, Mapping):
            extract_source = m.ConfigMap.model_validate({
                str(key): FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(item),
                )
                for key, item in value.items()
            })
        else:
            raise AssertionError(
                f"Path assertions require dict or model, got {type(value).__name__}",
            )
        extracted = u.extract(extract_source, path)
        if extracted.failure:
            raise AssertionError(
                c.Tests.ERR_SCOPE_PATH_NOT_FOUND.format(
                    path=path,
                    error=extracted.error,
                ),
            )
        return FlextTestsPayloadUtilities.to_payload(extracted.value)

    @staticmethod
    def _extract_attribute_path(
        value: object, attr_path: str
    ) -> t.Tests.TestobjectSerializable:
        """Extract one dotted attribute path from a runtime object."""
        current: object | t.Tests.TestobjectSerializable = value
        for segment in attr_path.split("."):
            if isinstance(current, Mapping) and segment in current:
                current = current[segment]
                continue
            if not hasattr(current, segment):
                raise AssertionError(f"Object missing attribute path: {attr_path}")
            current = getattr(current, segment)
        return FlextTestsPayloadUtilities.to_payload(current)

    @staticmethod
    def _apply_rule(
        subject: t.Tests.TestobjectSerializable | m.BaseModel | t.Tests.Testobject,
        rule: t.Tests.MatchRuleSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        """Apply one declarative rule by delegating to tm.that()."""
        FlextTestsMatchersUtilities.Tests.Matchers.that(
            subject,
            **FlextTestsMatchersUtilities._rule_to_kwargs(
                rule,
                inherited_msg=inherited_msg,
            ),
        )

    @staticmethod
    def _apply_path_rules(
        subject: t.Tests.TestobjectSerializable
        | m.BaseModel
        | Mapping[str, t.Tests.TestobjectSerializable],
        rules: t.Tests.PathMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        """Apply multiple dotted-path assertions against a mapping/model subject."""
        for path, rule in rules.items():
            try:
                extracted = FlextTestsMatchersUtilities._extract_mapping_path(
                    subject, path
                )
                FlextTestsMatchersUtilities._apply_rule(
                    extracted,
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Path rule '{path}' failed: {exc}",
                ) from exc

    @staticmethod
    def _apply_item_rules(
        subject: t.Tests.TestobjectSerializable
        | Sequence[t.Tests.TestobjectSerializable],
        rules: t.Tests.ItemMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        """Apply selector-based assertions against a sequence subject."""
        if not isinstance(subject, Sequence) or isinstance(
            subject, (str, bytes, bytearray)
        ):
            raise AssertionError(
                inherited_msg
                or f"Item assertions require a sequence, got {type(subject).__name__}",
            )
        sequence_value = list(subject)
        if isinstance(rules, Sequence) and not isinstance(
            rules, (str, bytes, bytearray)
        ):
            for index, rule in enumerate(rules):
                FlextTestsMatchersUtilities._apply_rule(
                    sequence_value[index],
                    rule,
                    inherited_msg=inherited_msg,
                )
            return
        if not isinstance(rules, Mapping):
            raise AssertionError(
                inherited_msg
                or "Item assertions must be a sequence or selector mapping",
            )
        for selector, rule in rules.items():
            if selector in {"*", "all"}:
                for item in sequence_value:
                    FlextTestsMatchersUtilities._apply_rule(
                        item,
                        rule,
                        inherited_msg=inherited_msg,
                    )
                continue
            if selector == "first":
                target_index = 0
            elif selector == "last":
                target_index = -1
            else:
                target_index = int(selector)
            FlextTestsMatchersUtilities._apply_rule(
                sequence_value[target_index],
                rule,
                inherited_msg=inherited_msg,
            )

    @staticmethod
    def _apply_attribute_rules(
        subject: object,
        rules: t.Tests.AttributeMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        """Apply multiple dotted-attribute assertions against an object subject."""
        for attr_path, rule in rules.items():
            try:
                attr_value = FlextTestsMatchersUtilities._extract_attribute_path(
                    subject,
                    attr_path,
                )
                FlextTestsMatchersUtilities._apply_rule(
                    attr_value,
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Attribute rule '{attr_path}' failed: {exc}",
                ) from exc

    @staticmethod
    def _is_non_string_sequence(
        value: t.Tests.TestobjectSerializable
        | t.Tests.MatcherKwargValue
        | t.JsonPayload
        | t.JsonValue,
    ) -> TypeIs[Sequence[t.Tests.TestobjectSerializable]]:
        return isinstance(value, Sequence) and (
            not isinstance(value, (str, bytes, bytearray))
        )

    @staticmethod
    def _check_has_lacks(
        value: object,
        has: t.Tests.ContainmentSpec | t.Tests.MatcherKwargValue | t.JsonValue | None,
        lacks: t.Tests.ContainmentSpec | t.Tests.MatcherKwargValue | t.JsonValue | None,
        msg: str | None,
        *,
        as_str: bool = False,
    ) -> None:
        """Shared has/lacks containment check for ok(), fail(), and that()."""
        if has is not None:
            items: Sequence[
                t.Tests.TestobjectSerializable | t.Tests.MatcherKwargValue | t.JsonValue
            ] = (
                list(has)
                if FlextTestsMatchersUtilities._is_non_string_sequence(has)
                else [has]
            )
            for item in items:
                if as_str:
                    check_str = str(item)
                    target = str(value)
                    if check_str not in target:
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_CONTAINS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )
                else:
                    check_val = FlextTestsPayloadUtilities.to_payload(item)
                    target_raw = FlextTestsPayloadUtilities.to_payload(value)
                    if isinstance(target_raw, m.RootModel):
                        target_raw = FlextTestsPayloadUtilities.to_payload(
                            target_raw.model_dump(),
                        )
                    if not isinstance(
                        target_raw,
                        (Mapping, str, list, tuple, set, frozenset),
                    ):
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_CONTAINS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )
                    if isinstance(target_raw, (set, frozenset, tuple)):
                        if check_val not in target_raw:
                            FlextTestsMatchersUtilities._raise_match_assertion(
                                c.Tests.ERR_CONTAINS_FAILED,
                                msg=msg,
                                container=value,
                                item=item,
                            )
                        continue
                    if isinstance(target_raw, str):
                        if str(check_val) not in target_raw:
                            FlextTestsMatchersUtilities._raise_match_assertion(
                                c.Tests.ERR_CONTAINS_FAILED,
                                msg=msg,
                                container=value,
                                item=item,
                            )
                    elif check_val not in target_raw:
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_CONTAINS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )
        if lacks is not None:
            items = (
                list(lacks)
                if FlextTestsMatchersUtilities._is_non_string_sequence(lacks)
                else [lacks]
            )
            for item in items:
                if as_str:
                    check_str = str(item)
                    target = str(value)
                    if check_str in target:
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_LACKS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )
                else:
                    check_val = FlextTestsPayloadUtilities.to_payload(item)
                    target_raw_2 = FlextTestsPayloadUtilities.to_payload(value)
                    if isinstance(target_raw_2, m.RootModel):
                        target_raw_2 = FlextTestsPayloadUtilities.to_payload(
                            target_raw_2.model_dump(),
                        )
                    if not isinstance(target_raw_2, (Mapping, str, list)):
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_LACKS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )
                    if isinstance(target_raw_2, str):
                        if str(check_val) in target_raw_2:
                            FlextTestsMatchersUtilities._raise_match_assertion(
                                c.Tests.ERR_LACKS_FAILED,
                                msg=msg,
                                container=value,
                                item=item,
                            )
                    elif check_val in target_raw_2:
                        FlextTestsMatchersUtilities._raise_match_assertion(
                            c.Tests.ERR_LACKS_FAILED,
                            msg=msg,
                            container=value,
                            item=item,
                        )

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers:
            """Test matchers with powerful generalist methods.

            Short alias: tm

            Core Methods (5 main methods):
                tm.ok(result, **kw)     - Assert r success, optional validation
                tm.fail(result, **kw)   - Assert r failure, optional validation
                tm.check(result)        - Railway-pattern chained assertions
                tm.that(value, **kw)    - Universal assertion - ALL validations in ONE method
                tm.scope()              - Isolated test context (context manager)

            The tm.that() method handles ALL assertion types:
                - Comparisons: eq, ne, gt, gte, lt, lte
                - Type/None: is_, none
                - Containment: contains (works for dict/list/str)
                - Strings: starts, ends, match, excludes
                - Length: length, length_gt, length_gte, length_lt, length_lte, empty

            Deprecated Methods (all redirect to tm.that()):
                tm.that() -> tm.that(actual, eq=eq=expected)
                tm.true() -> tm.that(condition, eq=True)
                tm.assert_contains() -> tm.that(container, contains=item)
                tm.str_() -> tm.that(text, contains/starts/ends/match/excludes/empty=...)
                tm.is_() -> tm.that(value, is_=type, none=...)
                tm.len() -> tm.that(items, length/length_gt/length_gte/empty=...)
                tm.hasattr() -> tm.that(hasattr(obj, attr), eq=True)
                tm.method() -> tm.that(hasattr(...), eq=True) + tm.that(callable(...), eq=True)
                tm.not_none() -> tm.that(value, none=False)
                tm.dict_() -> tm.that(data, contains=...) or tm.that(data, length=...)
                tm.that() -> tm.that(items, has=...) or tm.that(items, length=...)
                tm.that() -> tm.that(value, is_=is_=type, none=False, none=False)
            """

            @staticmethod
            def assert_result_success[TResult](
                result: FlextProtocolsResult.Result[TResult],
                msg: str | None = None,
            ) -> TResult:
                """Assert result is success and return unwrapped value.

                Args:
                    result: r to check
                    msg: Optional custom error message

                Returns:
                    Unwrapped value from result

                Raises:
                    AssertionError: If result is failure

                """
                if not result.success:
                    error_msg = (
                        msg or f"Expected success but got failure: {result.error}"
                    )
                    raise AssertionError(error_msg)
                return result.value

            @staticmethod
            def check[TResult](
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
            def fail[TResult](
                result: p.Result[TResult],
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> str:
                r"""Enhanced assertion for r failure with optional error validation.

                Examples:
                    # Basic failure assertions
                    tm.fail(result)                   # Assert failure
                    tm.fail(result, has="not found")  # Failure with error containing
                    tm.fail(result, code="VALIDATION")  # Failure with specific code
                    tm.fail(result, match=r"Error: \\\\d+")  # Error matches regex

                    # Multiple error checks
                    tm.fail(result, has=["invalid", "required"], lacks="internal")

                    # Error metadata checks
                    tm.fail(result, code="VALIDATION", data={"field": "email"})

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

                Uses Pydantic 2 models for parameter validation and computation.
                All parameters are validated via m.Tests.FailParams model.

                """
                try:
                    params = m.Tests.FailParams.model_validate(kwargs)
                except (TypeError, ValueError, AttributeError) as exc:
                    raise ValueError(f"Parameter validation failed: {exc}") from exc
                if result.success:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_FAIL_EXPECTED.format(value=result.value),
                    )
                err = result.error or ""
                if (
                    params.has
                    or params.lacks
                    or params.starts
                    or params.ends
                    or params.match
                ):
                    FlextTestsMatchersUtilities._check_has_lacks(
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
                    if params.match is not None and (
                        not u.chk(err, m.GuardCheckSpec(match=params.match))
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_NOT_MATCHES.format(
                                text=err,
                                pattern=params.match,
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
                        items_list = [str(x) for x in code_has_value]
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
                            str(k): FlextTestsPayloadUtilities.to_payload(v)
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
            def ok[TResult](
                result: FlextProtocolsResult.Result[TResult],
            ) -> TResult: ...

            @staticmethod
            @overload
            def ok[TResult](
                result: FlextProtocolsResult.Result[TResult],
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> TResult | t.Tests.TestobjectSerializable: ...

            @staticmethod
            def ok[TResult](
                result: FlextProtocolsResult.Result[TResult],
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

                Notes:
                    Uses Pydantic 2 models for parameter validation and computation.
                    All parameters are validated via m.Tests.OkParams model.

                Examples:
                    # Basic success assertions
                    tm.ok(result)                      # Assert success
                    tm.ok(result, eq=5)               # Success and value == 5
                    tm.ok(result, is_=str, len=(1,100))  # Success, is string, len 1-100
                    tm.ok(result, has=["a", "b"])     # Success and value contains both

                    # Deep structural matching on result value
                    tm.ok(result, deep={
                        "user.name": "John",
                        "user.email": lambda e: "@" in e,
                    })

                    # Path extraction first
                    tm.ok(result, path="data.value", eq=42)

                    # Custom validation
                    tm.ok(result, where=lambda x: x.status == "active")

                    Parameters validated via m.Tests.OkParams model:
                    - eq, ne: Equality/inequality check
                    - is_: Runtime type check against single type or tuple
                    - none, empty: Nullability checks
                    - gt, gte, lt, lte: Comparison checks (numeric or length)
                    - has, lacks: Unified containment (replaces contains)
                    - starts, ends, match: String assertions
                    - len: Length spec - exact int or (min, max) tuple
                    - deep: Deep structural matching specification
                    - path: Extract nested value via dot notation before validation
                    - where: Custom predicate function for validation
                    - msg: Custom error message
                    - contains, starts, ends: Legacy parameters (deprecated)

                """
                try:
                    params = m.Tests.OkParams.model_validate(kwargs)
                except (TypeError, ValueError, AttributeError) as exc:
                    raise ValueError(f"Parameter validation failed: {exc}") from exc
                if not result.success:
                    raise AssertionError(
                        params.msg or c.Tests.ERR_OK_FAILED.format(error=result.error),
                    )
                result_value: TResult | t.Tests.TestobjectSerializable = result.value
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
                    extract_data: m.ConfigMap
                    if isinstance(result_value, m.BaseModel):
                        extract_data = m.ConfigMap.model_validate(
                            result_value.model_dump(mode="python"),
                        )
                    else:
                        try:
                            extract_data = m.ConfigMap.model_validate(result_value)
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
                        FlextTestsMatchersUtilities._prepare_eq_ne_payloads(
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
                            "match": params.match,
                        }),
                    ):
                        error_msg = (
                            params.msg
                            or f"Value {result_value!r} did not satisfy constraints"
                        )
                        raise AssertionError(error_msg)
                if (
                    params.is_ is not None
                    and isinstance(params.is_, tuple)
                    and not any(
                        FlextTestsMatchersUtilities._matches_runtime_type(
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
                FlextTestsMatchersUtilities._check_has_lacks(
                    result_value,
                    params.has,
                    params.lacks,
                    params.msg,
                )
                result_payload = FlextTestsPayloadUtilities.to_payload(
                    result_value,
                )
                if params.len is not None:
                    FlextTestsMatchersUtilities._assert_len_match(
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
                        m.BaseModel | Mapping[str, t.Tests.TestobjectSerializable]
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
                    FlextTestsMatchersUtilities._apply_path_rules(
                        result_payload,
                        params.paths,
                        inherited_msg=params.msg,
                    )
                if params.items is not None:
                    FlextTestsMatchersUtilities._apply_item_rules(
                        result_payload,
                        params.items,
                        inherited_msg=params.msg,
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersUtilities._apply_attribute_rules(
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

            @staticmethod
            @contextmanager
            def scope(
                **kwargs: t.Tests.TestobjectSerializable,
            ) -> Generator[m.Tests.TestScope]:
                """Enhanced isolated test execution scope.

                Uses Pydantic 2 model (ScopeParams) for parameter validation and computation.
                All parameters are validated automatically via from_kwargs.

                Provides isolated configuration, container, and context for tests.
                Supports temporary environment variables, working directory changes,
                and automatic cleanup functions.

                Args:
                    **kwargs: Parameters validated via m.ScopeParams model
                        - settings: Initial configuration values
                        - container: Initial container/service mappings
                        - context: Initial context values
                        - cleanup: Sequence of cleanup functions to call on exit
                        - env: Temporary environment variables (restored on exit)
                        - cwd: Temporary working directory (restored on exit)

                Yields:
                    TestScope with settings, container, and context dicts

                Examples:
                    with tm.scope() as s:
                        s.container["service"] = mock_service
                        result = operation()
                        tm.ok(result)

                    with tm.scope(settings={"debug": True}, env={"API_KEY": "test"}) as s:
                        # Test with specific settings and env vars
                        pass

                    with tm.scope(cleanup=[lambda: cleanup_resource()]) as s:
                        # Auto-cleanup on exit
                        pass

                Raises:
                    ValueError: If parameter validation fails (via Pydantic model)

                """
                try:
                    params = m.Tests.ScopeParams.model_validate(kwargs)
                except (TypeError, ValueError, AttributeError) as exc:
                    raise ValueError(f"Parameter validation failed: {exc}") from exc
                original_cwd: Path | None = None
                env_context = (
                    FlextTestsConfigHelpersUtilitiesMixin.env_vars_context(params.env)
                    if params.env is not None
                    else nullcontext()
                )
                try:
                    with env_context:
                        if params.cwd is not None:
                            original_cwd = Path.cwd()
                            cwd_path = (
                                Path(params.cwd)
                                if u.matches_type(params.cwd, "str")
                                else params.cwd
                            )
                            os.chdir(cwd_path)
                        cfg: Mapping[str, t.Tests.TestobjectSerializable] = {}
                        if params.settings:
                            cfg = {
                                str(key): value
                                for key, value in params.settings.items()
                            }
                        container_dict = {
                            k: v
                            for k, v in (params.container or {}).items()
                            if t.Tests.general_value(v)
                        }
                        context_map: Mapping[str, t.Tests.TestobjectSerializable] = {}
                        if params.context:
                            context_map = {
                                str(key): value for key, value in params.context.items()
                            }
                        yield m.Tests.TestScope.model_validate({
                            "settings": cfg,
                            "container": container_dict,
                            "context": context_map,
                        })
                finally:
                    if original_cwd is not None:
                        os.chdir(original_cwd)
                    if params.cleanup is not None:
                        for cleanup_func in params.cleanup:
                            try:
                                cleanup_func()
                            except (
                                OSError,
                                RuntimeError,
                                TypeError,
                                ValueError,
                                AttributeError,
                            ) as e:
                                warnings.warn(
                                    c.Tests.ERR_SCOPE_CLEANUP_FAILED.format(
                                        error=str(e),
                                    ),
                                    RuntimeWarning,
                                    stacklevel=2,
                                )

            @staticmethod
            def that(
                value: object,
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> None:
                r"""Super-powered universal value assertion - ALL validations in ONE method.

                This is the PRIMARY assertion method. All other assertion methods
                (eq, true, assert_contains, str_, is_, len, etc.) are convenience
                wrappers that delegate to this method.

                Supports unlimited depth for deep structural matching, comprehensive
                collection assertions, mapping validations, and custom predicates.

                Examples:
                    # Basic assertions
                    tm.that(x, eq=5)                    # x == 5
                    tm.that(x, is_=str, len=(1, 50))    # is string, len 1-50
                    tm.that(x, gt=0, lt=100)            # 0 < x < 100

                    # String assertions
                    tm.that(text, starts="Hello", ends="!", len=(5, 100))
                    tm.that(email, match=r"^[\\w.]+@[\\w.]+$")

                    # Sequence assertions
                    tm.that(items, len=5, first="a", last="z", unique=True)
                    tm.that(items, all_=str, sorted=True)
                    tm.that(items, has=["required1", "required2"])

                    # Mapping assertions
                    tm.that(data, keys=["id", "name"], kv={"status": "active"})
                    tm.that(settings, attrs=["debug", "timeout"], attr_eq={"debug": True})

                    # r in tm.that() (auto-detected)
                    tm.that(result, ok=True, eq="expected")

                    # Deep structural matching (unlimited depth)
                    tm.that(response, deep={
                        "user.name": "John",
                        "user.profile.address.city": "NYC",
                        "user.email": lambda e: "@" in e,
                        "items": lambda i: len(i) > 0,
                    })

                    # Custom validation
                    tm.that(user, where=lambda u: u.age >= 18 and u.verified)

                Args:
                    value: Value to validate
                    msg: Custom error message
                    eq, ne: Equality/inequality
                    is_, not_: Type checks - supports single type or tuple
                    none: None check (True=must be None, False=must not be None)
                    empty: Empty check (True=must be empty, False=must not be empty)
                    gt, gte, lt, lte: Comparisons (numeric or length)
                    len: Unified length spec - exact int or (min, max) tuple
                    has: Unified containment - value contains item(s) (replaces contains)
                    lacks: Unified non-containment - value does NOT contain item(s) (replaces excludes)
                    starts, ends: String prefix/suffix
                    match: Regex pattern (for strings)
                    first, last: Sequence first/last item equals
                    all_: All items match type or predicate
                    any_: At least one item matches type or predicate
                    sorted: Is sorted (True=ascending, or key function)
                    unique: All items unique
                    keys: Mapping has all keys
                    lacks_keys: Mapping missing keys
                    values: Mapping has all values
                    kv: Key-value pairs (single tuple or mapping)
                    attrs: Object has attribute(s)
                    methods: Object has method(s)
                    attr_eq: Attribute equals (single tuple or mapping)
                    ok: For r: assert success
                    error: For r: error contains
                    deep: Deep structural matching specification
                    where: Custom predicate function
                    contains, excludes, length, length_gt, etc.: Legacy parameters (deprecated)

                Raises:
                    AssertionError: If value doesn't satisfy constraints
                    ValueError: If parameter validation fails (via Pydantic model)

                """
                raw_eq: t.Tests.MatcherKwargValue | None = (
                    kwargs.get("eq") if "eq" in kwargs else None
                )
                raw_ne: t.Tests.MatcherKwargValue | None = (
                    kwargs.get("ne") if "ne" in kwargs else None
                )
                raw_has: t.Tests.MatcherKwargValue | None = (
                    kwargs.get("has") if "has" in kwargs else None
                )
                raw_contains: t.Tests.MatcherKwargValue | None = (
                    kwargs.get("contains") if "contains" in kwargs else None
                )
                try:
                    params = m.Tests.ThatParams.model_validate(kwargs)
                except (TypeError, ValueError, AttributeError):
                    non_serializable_keys = {
                        "eq",
                        "ne",
                        "has",
                        "contains",
                        "lacks",
                        "excludes",
                    }
                    filtered_kwargs = {
                        key: val
                        for key, val in kwargs.items()
                        if key not in non_serializable_keys
                    }
                    try:
                        params = m.Tests.ThatParams.model_validate(filtered_kwargs)
                    except (TypeError, ValueError, AttributeError) as filtered_exc:
                        raise ValueError(
                            f"Parameter validation failed: {filtered_exc}",
                        ) from filtered_exc
                # Early is_/not_ checks on the ORIGINAL value before any
                # conversion — _to_test_payload may coerce types (e.g.
                # Exception → str) which breaks isinstance checks.
                value_type_name = type(value).__name__
                if params.is_ is not None:
                    is_types = (
                        params.is_ if isinstance(params.is_, tuple) else (params.is_,)
                    )
                    root_value = getattr(value, "root", None)
                    is_mapping_wrapper = (
                        dict in is_types
                        and isinstance(root_value, dict)
                        and value.__class__.__name__ == "Dict"
                    )
                    is_model_mapping = (
                        dict in is_types
                        and isinstance(value, m.BaseModel)
                        and not isinstance(value, m.RootModel)
                    )
                    is_sequence_wrapper = (
                        list in is_types
                        and isinstance(root_value, (list, tuple))
                        and value_type_name == "ObjectList"
                    )
                    matches_declared_type = any(
                        FlextTestsMatchersUtilities._matches_runtime_type(
                            value,
                            expected_type,
                        )
                        for expected_type in is_types
                    )
                    if (
                        not matches_declared_type
                        and not is_mapping_wrapper
                        and not is_model_mapping
                        and not is_sequence_wrapper
                    ):
                        raise AssertionError(
                            params.msg
                            or f"Assertion failed: {c.Tests.ERR_TYPE_FAILED.format(expected=params.is_, actual=value_type_name)}",
                        )
                if params.not_ is not None:
                    not_types = (
                        params.not_
                        if isinstance(params.not_, tuple)
                        else (params.not_,)
                    )
                    if any(
                        FlextTestsMatchersUtilities._matches_runtime_type(
                            value,
                            forbidden_type,
                        )
                        for forbidden_type in not_types
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_TYPE_FAILED.format(
                                expected=f"not {params.not_}",
                                actual=value_type_name,
                            ),
                        )
                # If is_/not_ was the only validation, return early —
                # skip r unwrap which assumes ok/has.
                only_type_check = (
                    (params.is_ is not None or params.not_ is not None)
                    and params.ok is None
                    and params.has is None
                    and params.lacks is None
                    and params.eq is None
                    and raw_eq is None
                    and params.ne is None
                    and raw_ne is None
                    and params.gt is None
                    and params.gte is None
                    and params.lt is None
                    and params.lte is None
                    and params.none is None
                    and params.empty is None
                    and params.starts is None
                    and params.ends is None
                    and params.match is None
                    and params.len is None
                )
                if only_type_check:
                    return
                subject = value
                if isinstance(subject, p.Result):
                    result_obj = subject
                    actual_value: t.Tests.TestobjectSerializable | str = ""
                    if params.ok is not None:
                        if params.ok and (not result_obj.success):
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_OK_FAILED.format(
                                    error=result_obj.error,
                                ),
                            )
                        if not params.ok and result_obj.success:
                            value_str: str = str(result_obj.value)
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_FAIL_EXPECTED.format(
                                    value=value_str,
                                ),
                            )
                        if result_obj.success:
                            actual_value = getattr(result_obj, "value", "")
                    elif params.has is not None:
                        err = result_obj.error or ""
                        FlextTestsMatchersUtilities._check_has_lacks(
                            err,
                            params.has,
                            None,
                            params.msg,
                            as_str=True,
                        )
                        actual_value = err
                    elif result_obj.success:
                        actual_value = getattr(result_obj, "value", "")
                    else:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_OK_FAILED.format(
                                error=result_obj.error,
                            ),
                        )
                    subject = actual_value
                subject_payload = FlextTestsPayloadUtilities.to_payload(subject)
                has_validation = (
                    raw_eq is not None
                    or raw_ne is not None
                    or params.eq is not None
                    or (params.ne is not None)
                    or (params.gt is not None)
                    or (params.gte is not None)
                    or (params.lt is not None)
                    or (params.lte is not None)
                    or (params.none is not None)
                    or (params.empty is not None)
                    or (params.starts is not None)
                    or (params.ends is not None)
                    or (params.match is not None)
                )
                if has_validation:
                    chk_subject_payload = (
                        None
                        if params.none is True and subject_payload == ""
                        else subject_payload
                    )
                    eq_value = raw_eq if "eq" in kwargs else params.eq
                    ne_value = raw_ne if "ne" in kwargs else params.ne
                    eq_payload, ne_payload = (
                        FlextTestsMatchersUtilities._prepare_eq_ne_payloads(
                            subject_payload,
                            eq_value,
                            ne_value,
                            msg=params.msg,
                            default_msg=(
                                f"Assertion failed: {subject_payload!r} did not satisfy constraints"
                            ),
                        )
                    )
                    eq_plain2 = (
                        FlextTestsPayloadUtilities.to_normalized_value(eq_payload)
                        if eq_payload is not None
                        else None
                    )
                    ne_plain2 = (
                        FlextTestsPayloadUtilities.to_normalized_value(ne_payload)
                        if ne_payload is not None
                        else None
                    )
                    chk_subject_plain: t.GuardInput | None = (
                        None
                        if chk_subject_payload is None
                        else FlextTestsPayloadUtilities.to_normalized_value(
                            chk_subject_payload,
                        )
                    )
                    if not u.chk(
                        chk_subject_plain,
                        m.GuardCheckSpec.model_validate({
                            "eq": eq_plain2,
                            "ne": ne_plain2,
                            "gt": params.gt,
                            "gte": params.gte,
                            "lt": params.lt,
                            "lte": params.lte,
                            "none": params.none,
                            "empty": params.empty,
                            "starts": params.starts,
                            "ends": params.ends,
                            "match": params.match,
                        }),
                    ):
                        error_msg = (
                            params.msg
                            or f"Assertion failed: {subject_payload!r} did not satisfy constraints"
                        )
                        raise AssertionError(error_msg)
                # is_/not_ checks are handled early (before result
                # detection) to avoid _to_test_payload coercion issues.
                effective_has = (
                    raw_has
                    if raw_has is not None
                    else (raw_contains if raw_contains is not None else params.has)
                )
                FlextTestsMatchersUtilities._check_has_lacks(
                    subject_payload,
                    effective_has,
                    params.lacks,
                    params.msg,
                )
                value_payload = subject_payload
                if params.len is not None:
                    FlextTestsMatchersUtilities._assert_len_match(
                        payload=value_payload,
                        sized=subject_payload,
                        length_spec=params.len,
                        msg=params.msg,
                    )
                if isinstance(subject_payload, (list, tuple)):
                    seq_value: Sequence[t.Tests.TestobjectSerializable] = []
                    try:
                        seq_value = t.Tests.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER.validate_python(
                            subject_payload,
                        )
                    except c.ValidationError:
                        pass
                    if params.first is not None:
                        if not seq_value:
                            raise AssertionError(
                                params.msg or "Sequence is empty, cannot check first",
                            )
                        if seq_value[0] != params.first:
                            raise AssertionError(
                                params.msg
                                or f"First item: expected {params.first!r}, got {seq_value[0]!r}",
                            )
                    if params.last is not None:
                        if not seq_value:
                            raise AssertionError(
                                params.msg or "Sequence is empty, cannot check last",
                            )
                        if seq_value[-1] != params.last:
                            raise AssertionError(
                                params.msg
                                or f"Last item: expected {params.last!r}, got {seq_value[-1]!r}",
                            )
                    if params.all_ is not None:
                        if isinstance(params.all_, type):
                            all_type = params.all_
                            if not all(isinstance(x, all_type) for x in seq_value):
                                failed_idx = next(
                                    (
                                        i
                                        for i, item in enumerate(seq_value)
                                        if not isinstance(item, all_type)
                                    ),
                                    None,
                                )
                                raise AssertionError(
                                    params.msg
                                    or c.Tests.ERR_ALL_ITEMS_FAILED.format(
                                        index=failed_idx,
                                    ),
                                )
                        elif callable(params.all_) and (
                            not all(
                                params.all_(
                                    FlextTestsPayloadUtilities.to_payload(item),
                                )
                                for item in seq_value
                            )
                        ):
                            failed_idx = next(
                                (
                                    i
                                    for i, item in enumerate(list(seq_value))
                                    if not params.all_(
                                        FlextTestsPayloadUtilities.to_payload(
                                            item,
                                        ),
                                    )
                                ),
                                None,
                            )
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_ALL_ITEMS_FAILED.format(
                                    index=failed_idx,
                                ),
                            )
                    if params.any_ is not None:
                        if isinstance(params.any_, type):
                            any_type = params.any_
                            if not any(
                                isinstance(item, any_type) for item in seq_value
                            ):
                                raise AssertionError(
                                    params.msg or c.Tests.ERR_ANY_ITEMS_FAILED,
                                )
                        elif callable(params.any_) and (
                            not any(
                                params.any_(
                                    FlextTestsPayloadUtilities.to_payload(item),
                                )
                                for item in seq_value
                            )
                        ):
                            raise AssertionError(
                                params.msg or c.Tests.ERR_ANY_ITEMS_FAILED,
                            )
                    sorted_param = params.sorted
                    if sorted_param is not None:
                        value_list = list(seq_value)
                        if sorted_param is True:
                            sorted_list = sorted(
                                value_list,
                                key=lambda x: (type(x).__name__, str(x)),
                            )
                            if value_list != sorted_list:
                                raise AssertionError(
                                    params.msg or "Sequence is not sorted",
                                )
                        elif callable(sorted_param):
                            user_key_fn = sorted_param

                            def comparable_key(
                                x: t.Tests.TestobjectSerializable,
                            ) -> tuple[str, str]:
                                """Wrap user key to return comparable tuple."""
                                result = user_key_fn(
                                    FlextTestsPayloadUtilities.to_payload(x),
                                )
                                type_name = type(result).__name__
                                return (str(type_name), str(result))

                            sorted_list = sorted(value_list, key=comparable_key)
                            if value_list != sorted_list:
                                raise AssertionError(
                                    params.msg
                                    or "Sequence is not sorted by key function",
                                )
                    if params.unique is not None and params.unique:
                        value_len = len(seq_value)
                        value_set_len = len(set(seq_value))
                        if value_len != value_set_len:
                            raise AssertionError(
                                params.msg or "Sequence contains duplicate items",
                            )
                if isinstance(subject_payload, Mapping):
                    mapping_value: Mapping[str, t.Tests.TestobjectSerializable] = {}
                    try:
                        mapping_value = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                            subject_payload,
                        )
                    except c.ValidationError:
                        pass
                    if params.keys is not None:
                        key_set: set[str] = set(params.keys)
                        missing = key_set - set(mapping_value.keys())
                        if missing:
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_KEYS_MISSING.format(
                                    keys=list(missing),
                                ),
                            )
                    if params.lacks_keys is not None:
                        lacks_key_set: set[str] = set(params.lacks_keys)
                        present = lacks_key_set & set(mapping_value.keys())
                        if present:
                            raise AssertionError(
                                params.msg
                                or c.Tests.ERR_KEYS_EXTRA.format(
                                    keys=list(present),
                                ),
                            )
                    if params.values is not None:
                        value_list = list(mapping_value.values())
                        for expected_val in params.values:
                            if expected_val not in value_list:
                                raise AssertionError(
                                    params.msg
                                    or f"Expected value {expected_val!r} not found in mapping",
                                )
                    if params.kv is not None:
                        match params.kv:
                            case tuple() as key_value if len(key_value) == 2:
                                key, expected_val = key_value
                                if key not in mapping_value:
                                    raise AssertionError(
                                        params.msg
                                        or f"Key {key!r} not found in mapping",
                                    )
                                if mapping_value[key] != expected_val:
                                    raise AssertionError(
                                        params.msg
                                        or f"Key {key!r}: expected {expected_val!r}, got {mapping_value[key]!r}",
                                    )
                            case Mapping() as mapping_kv:
                                for key, expected_obj in mapping_kv.items():
                                    if key not in mapping_value:
                                        raise AssertionError(
                                            params.msg
                                            or f"Key {key!r} not found in mapping",
                                        )
                                    if mapping_value[key] != expected_obj:
                                        raise AssertionError(
                                            params.msg
                                            or f"Key {key!r}: expected {expected_obj!r}, got {mapping_value[key]!r}",
                                        )
                if params.attrs is not None:
                    attrs_target = subject
                    if isinstance(params.attrs, str):
                        attr_list: t.StrSequence = [params.attrs]
                    else:
                        attr_list = list(params.attrs)
                    for attr in attr_list:
                        if not hasattr(attrs_target, attr):
                            raise AssertionError(
                                params.msg or f"Object missing attribute: {attr}",
                            )
                if params.methods is not None:
                    methods_target = subject
                    if isinstance(params.methods, str):
                        method_list: t.StrSequence = [params.methods]
                    else:
                        method_list = list(params.methods)
                    for method in method_list:
                        if not hasattr(methods_target, method):
                            raise AssertionError(
                                params.msg or f"Object missing method: {method}",
                            )
                        if not callable(getattr(methods_target, method)):
                            raise AssertionError(
                                params.msg
                                or f"Object attribute {method} is not callable",
                            )
                if params.attr_eq is not None:
                    attr_eq_target = subject
                    match params.attr_eq:
                        case tuple() as attr_spec if len(attr_spec) == 2:
                            attr, expected_val = attr_spec
                            if not hasattr(attr_eq_target, attr):
                                raise AssertionError(
                                    params.msg or f"Object missing attribute: {attr}",
                                )
                            actual_val = getattr(attr_eq_target, attr)
                            if actual_val != expected_val:
                                raise AssertionError(
                                    params.msg
                                    or f"Attribute {attr}: expected {expected_val!r}, got {actual_val!r}",
                                )
                        case Mapping() as attr_mapping:
                            for attr, expected_val in attr_mapping.items():
                                if not hasattr(attr_eq_target, attr):
                                    raise AssertionError(
                                        params.msg
                                        or f"Object missing attribute: {attr}",
                                    )
                                actual_val = getattr(attr_eq_target, attr)
                                if actual_val != expected_val:
                                    raise AssertionError(
                                        params.msg
                                        or f"Attribute {attr}: expected {expected_val!r}, got {actual_val!r}",
                                    )
                if params.deep is not None:
                    if not isinstance(subject_payload, (m.BaseModel, dict)):
                        raise AssertionError(
                            params.msg
                            or f"Deep matching requires dict or model, got {type(subject_payload).__name__}",
                        )
                    deep_value: (
                        m.BaseModel | Mapping[str, t.Tests.TestobjectSerializable]
                    )
                    if isinstance(subject_payload, m.BaseModel):
                        deep_value = subject_payload
                    else:
                        try:
                            deep_value = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                                subject_payload,
                            )
                        except c.ValidationError:
                            deep_value = dict[str, t.Tests.TestobjectSerializable]()
                    match_result = FlextTestsPayloadUtilities.deep_match(
                        deep_value, params.deep
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
                    FlextTestsMatchersUtilities._apply_path_rules(
                        subject_payload,
                        params.paths,
                        inherited_msg=params.msg,
                    )
                if params.items is not None:
                    FlextTestsMatchersUtilities._apply_item_rules(
                        subject_payload,
                        params.items,
                        inherited_msg=params.msg,
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersUtilities._apply_attribute_rules(
                        subject,
                        params.attrs_match,
                        inherited_msg=params.msg,
                    )
                if params.where is not None and (not params.where(subject_payload)):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_PREDICATE_FAILED.format(
                            value=subject_payload,
                        ),
                    )


tm = FlextTestsMatchersUtilities.Tests.Matchers
__all__: list[str] = ["FlextTestsMatchersUtilities", "tm"]
