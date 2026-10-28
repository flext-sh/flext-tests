"""Universal 'that' matcher utilities for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import ClassVar, TypeAliasType

from flext_cli import u

from flext_tests import c, m, p, t
from flext_tests._utilities import (
    FlextTestsPayloadUtilities,
    FlextTestsUtilitiesMatchersAssertions,
    FlextTestsUtilitiesMatchersContainment,
    FlextTestsUtilitiesMatchersTypeguards,
)


class FlextTestsUtilitiesMatchersThat:
    """Fluent matcher assertions."""

    _TUPLE_NAME_VALUE_PAIR_LEN: ClassVar[int] = 2

    class Tests:
        """Test utility namespace."""

        class Matchers:
            """Matcher assertion helpers."""

            @classmethod
            def _validate_declared_types(
                cls,
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate declared types with the caller's explicit ownership.

                Raises:
                    AssertionError: If
                        any declared forbidden type matches the original value.

                """
                if params.is_ is not None:
                    cls._validate_is_type(
                        value,
                        params,
                        type(value).__name__,
                    )
                if params.not_ is not None:
                    not_types = (
                        params.not_
                        if isinstance(params.not_, tuple)
                        else (params.not_,)
                    )
                    if isinstance(value, not_types):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_TYPE_FAILED.format(
                                expected=f"not {params.not_}",
                                actual=type(value).__name__,
                            ),
                        )

            @staticmethod
            def _validate_is_type(
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
                value_type_name: str,
            ) -> None:
                """Validate the actual runtime type without wrapper substitutions.

                Raises:
                    AssertionError: Always.

                """
                is_types = (
                    params.is_ if isinstance(params.is_, tuple) else (params.is_,)
                )
                expected_types = tuple(
                    item for item in is_types if isinstance(item, type)
                )
                if isinstance(value, expected_types):
                    return
                type_error = c.Tests.ERR_TYPE_FAILED.format(
                    expected=params.is_,
                    actual=value_type_name,
                )
                raise AssertionError(params.msg or f"Assertion failed: {type_error}")

            @staticmethod
            def _is_subject_only(
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> bool:
                """Recognize type/presence checks answered by the original subject.

                These criteria hold for any runtime object, so they never require
                a payload conversion. ``none`` against a result still unwraps it.

                Returns:
                    The resulting ``bool``.

                """
                subject_fields = {
                    "msg",
                    "is_",
                    "not_",
                    "none",
                    "attrs",
                    "methods",
                    "attr_eq",
                    "attrs_match",
                }
                if params.none is not None and u.result_view(value):
                    return False
                return all(
                    getattr(params, name) is None
                    for name in type(params).model_fields
                    if name not in subject_fields
                )

            @classmethod
            def _validate_subject_only(
                cls,
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> bool:
                """Apply presence and attribute rules to the original subject.

                Returns:
                    Whether the subject-only branch completed validation.

                Raises:
                    AssertionError: The original presence or attribute rule failed.

                """
                if not cls._is_subject_only(value, params):
                    return False
                if params.none is not None and (value is None) is not params.none:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_CONSTRAINTS_FAILED.format(value=value),
                    )
                if params.attrs_match is not None:
                    FlextTestsUtilitiesMatchersThat.apply_attribute_rules(
                        value,
                        params.attrs_match,
                        inherited_msg=params.msg,
                    )
                return True

            @classmethod
            def _result_subject[SubjectT](
                cls,
                subject: SubjectT,
                params: m.Tests.ThatParams,
            ) -> SubjectT | p.Tests.Payload:
                """Return the value to validate after result-aware unwrapping.

                Raises:
                    AssertionError: Always.

                """
                if not u.result_view(subject):
                    return subject
                result_obj: p.ResultView[p.AttributeProbe] = subject
                if params.ok is not None:
                    return FlextTestsPayloadUtilities.to_payload(
                        cls._ok_value(result_obj, params),
                    )
                if params.has is not None:
                    err = result_obj.error or ""
                    FlextTestsUtilitiesMatchersContainment.check_has_lacks(
                        err,
                        params.has,
                        None,
                        params.msg,
                        as_str=True,
                    )
                    return FlextTestsPayloadUtilities.to_payload(
                        err,
                    )
                if result_obj.success:
                    return FlextTestsPayloadUtilities.to_payload(
                        result_obj.value,
                    )
                raise AssertionError(
                    params.msg or c.Tests.ERR_OK_FAILED.format(error=result_obj.error),
                )

            @staticmethod
            def _ok_value[ValueT](
                result_obj: p.ResultView[ValueT],
                params: m.Tests.ThatParams,
            ) -> ValueT | str:
                """Validate result ok/fail expectation and return success value.

                Returns:
                    The resulting ``ValueT | str``.

                Raises:
                    AssertionError: If ``params.ok and (not result_obj.success)``; or if
                        ``not params.ok and result_obj.success``.

                """
                if params.ok and not result_obj.success:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_OK_FAILED.format(error=result_obj.error),
                    )
                if not params.ok and result_obj.success:
                    value_str = str(result_obj.value)
                    raise AssertionError(
                        params.msg or c.Tests.ERR_FAIL_EXPECTED.format(value=value_str),
                    )
                return result_obj.value if result_obj.success else ""

            @staticmethod
            def _has_scalar_validation(params: m.Tests.ThatParams) -> bool:
                """Return whether scalar guard validation is requested."""
                return any(
                    getattr(params, name) is not None
                    for name in c.Tests.MATCHER_SCALAR_CRITERIA
                )

            @staticmethod
            def _validate_common(
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
                *,
                effective_has: p.Tests.Payload | None,
            ) -> None:
                """Validate containment and length predicates."""
                FlextTestsUtilitiesMatchersContainment.check_has_lacks(
                    subject_payload,
                    effective_has,
                    params.lacks,
                    params.msg,
                )
                if params.len is not None:
                    FlextTestsUtilitiesMatchersAssertions.assert_len_match(
                        payload=subject_payload,
                        length_spec=params.len,
                        msg=params.msg,
                    )

            @staticmethod
            def _validate_sequence_edges(
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate first/last sequence predicates.

                Raises:
                    AssertionError: If ``not seq_value``; or if
                        ``FlextTestsPayloadUtilities.to_match_value(seq_value[0]) !=
                        FlextTestsPayloadUtilities.to_match_value(params.first)``; or if
                        ``FlextTestsPayloadUtilities.to_match_value(seq_value[-1]) !=
                        FlextTestsPayloadUtilities.to_match_value(params.last)``.

                """
                if params.first is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check first",
                        )
                    if FlextTestsPayloadUtilities.to_match_value(
                        seq_value[0],
                    ) != FlextTestsPayloadUtilities.to_match_value(
                        params.first,
                    ):
                        raise AssertionError(
                            params.msg
                            or (
                                f"First item: expected {params.first!r}, "
                                f"got {seq_value[0]!r}"
                            ),
                        )
                if params.last is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check last",
                        )
                    if FlextTestsPayloadUtilities.to_match_value(
                        seq_value[-1],
                    ) != FlextTestsPayloadUtilities.to_match_value(
                        params.last,
                    ):
                        raise AssertionError(
                            params.msg
                            or (
                                f"Last item: expected {params.last!r}, "
                                f"got {seq_value[-1]!r}"
                            ),
                        )

            @classmethod
            def _validate_sequence(
                cls,
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate sequence-specific predicates."""
                if subject_payload.kind in {"atom", "mapping"}:
                    return
                seq_value = subject_payload.items
                cls._validate_sequence_edges(seq_value, params)
                if params.all_ is not None:
                    cls._validate_all(seq_value, params)
                if params.any_ is not None:
                    cls._validate_any(seq_value, params)
                cls._validate_sequence_order(seq_value, params)

            @staticmethod
            def _validate_all(
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate that all sequence items match a predicate/type.

                Raises:
                    AssertionError: If ``isinstance(params.all_, type)``; or if
                        ``failed_idx is not None``.

                """
                if isinstance(params.all_, type):
                    all_type = params.all_
                    if all(
                        isinstance(
                            FlextTestsPayloadUtilities.to_match_value(
                                item,
                            ),
                            all_type,
                        )
                        for item in seq_value
                    ):
                        return
                    failed_idx = next(
                        (
                            index
                            for index, item in enumerate(seq_value)
                            if not isinstance(
                                FlextTestsPayloadUtilities.to_match_value(
                                    item,
                                ),
                                all_type,
                            )
                        ),
                        None,
                    )
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx),
                    )
                if callable(params.all_):
                    predicate = params.all_
                    failed_idx = next(
                        (
                            index
                            for index, item in enumerate(seq_value)
                            if not predicate(
                                FlextTestsPayloadUtilities.to_match_value(
                                    item,
                                ),
                            )
                        ),
                        None,
                    )
                    if failed_idx is not None:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx),
                        )

            @staticmethod
            def _validate_any(
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate that any sequence item matches a predicate/type.

                Raises:
                    AssertionError: If ``callable(params.any_) and (not
                        any((params.any_(FlextTestsPayloadUtilities.to_match_value(
                            item
                        )) for item in seq_value)))``; or if ``not
                        any((isinstance(FlextTestsPayloadUtilities.to_match_value(item),
                        any_type) for item in seq_value))``.

                """
                if isinstance(params.any_, type):
                    any_type = params.any_
                    if not any(
                        isinstance(
                            FlextTestsPayloadUtilities.to_match_value(
                                item,
                            ),
                            any_type,
                        )
                        for item in seq_value
                    ):
                        raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)
                    return
                if callable(params.any_) and not any(
                    params.any_(
                        FlextTestsPayloadUtilities.to_match_value(
                            item,
                        ),
                    )
                    for item in seq_value
                ):
                    raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)

            @classmethod
            def _validate_sequence_order(
                cls,
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate sorted/unique sequence predicates.

                Raises:
                    AssertionError: If ``params.unique is not None and params.unique and
                        any((FlextTestsPayloadUtilities.to_match_value(item) ==
                        FlextTestsPayloadUtilities.to_match_value(previous) for index,
                        item in enumerate(seq_value) for previous in
                        seq_value[:index]))``; or if ``value_list != sorted_list``.

                """
                sorted_param = params.sorted
                if sorted_param is not None:
                    value_list = list(seq_value)
                    if sorted_param is True:
                        sorted_list = sorted(
                            value_list,
                            key=lambda item: cls._sort_key(
                                FlextTestsPayloadUtilities.to_match_value(item),
                            ),
                        )
                        if value_list != sorted_list:
                            raise AssertionError(params.msg or "Sequence is not sorted")
                    elif callable(sorted_param):
                        sorted_list = sorted(
                            value_list,
                            key=lambda item: cls._sort_key(
                                sorted_param(
                                    FlextTestsPayloadUtilities.to_match_value(item),
                                ),
                            ),
                        )
                        if value_list != sorted_list:
                            raise AssertionError(
                                params.msg or "Sequence is not sorted by key function",
                            )
                if (
                    params.unique is not None
                    and params.unique
                    and any(
                        FlextTestsPayloadUtilities.to_match_value(
                            item,
                        )
                        == FlextTestsPayloadUtilities.to_match_value(
                            previous,
                        )
                        for index, item in enumerate(seq_value)
                        for previous in seq_value[:index]
                    )
                ):
                    raise AssertionError(
                        params.msg or "Sequence contains duplicate items",
                    )

            @staticmethod
            def _sort_key(native: p.Tests.NativeMatchValue) -> t.StrPair:
                """Return a deterministic key for heterogeneous matcher values."""
                return type(native).__name__, str(native)

            @classmethod
            def _validate_mapping(
                cls,
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate mapping-specific predicates.

                Raises:
                    AssertionError: If ``missing``; or if ``present``; or if
                        ``FlextTestsPayloadUtilities.to_match_value(expected_val) not in
                        value_list``.

                """
                if subject_payload.kind != "mapping":
                    return
                mapping_value = subject_payload.entries
                if params.keys is not None:
                    missing = set(params.keys) - set(mapping_value.keys())
                    if missing:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_KEYS_MISSING.format(keys=list(missing)),
                        )
                if params.lacks_keys is not None:
                    present = set(params.lacks_keys) & set(mapping_value.keys())
                    if present:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_KEYS_EXTRA.format(keys=list(present)),
                        )
                if params.values is not None:
                    value_list = [
                        FlextTestsPayloadUtilities.to_match_value(
                            item,
                        )
                        for item in mapping_value.values()
                    ]
                    for expected_val in params.values:
                        if (
                            FlextTestsPayloadUtilities.to_match_value(
                                expected_val,
                            )
                            not in value_list
                        ):
                            raise AssertionError(
                                params.msg
                                or (
                                    f"Expected value {expected_val!r} "
                                    "not found in mapping"
                                ),
                            )
                if params.kv is not None:
                    cls._validate_kv(mapping_value, params)

            @staticmethod
            def _validate_kv(
                mapping_value: t.MappingKV[str, p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Compare owned mapping values through native projections.

                Raises:
                    AssertionError: If ``key not in mapping_value``; or if ``actual !=
                        wanted``.

                """
                if params.kv is None:
                    return
                for key, expected in FlextTestsUtilitiesMatchersThat._named_operands(
                    params.kv,
                ):
                    if key not in mapping_value:
                        raise AssertionError(
                            params.msg or f"Key {key!r} not found in mapping",
                        )
                    actual = FlextTestsPayloadUtilities.to_match_value(
                        mapping_value[key],
                    )
                    wanted = FlextTestsPayloadUtilities.to_match_value(
                        expected,
                    )
                    if actual != wanted:
                        raise AssertionError(
                            params.msg
                            or f"Key {key!r}: expected {wanted!r}, got {actual!r}",
                        )

            @classmethod
            def _validate_attrs(
                cls,
                subject: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate attrs/methods/attr_eq predicates.

                Raises:
                    AssertionError: If ``not hasattr(subject, attr)``; or if ``not
                        hasattr(subject, method)``; or if ``params.methods is not
                        None``.

                """
                if params.attrs is not None:
                    attr_list: t.StrSequence = (
                        [params.attrs]
                        if isinstance(params.attrs, str)
                        else list(params.attrs)
                    )
                    for attr in attr_list:
                        if not hasattr(subject, attr):
                            raise AssertionError(
                                params.msg or f"Object missing attribute: {attr}",
                            )
                if params.methods is not None:
                    method_list: t.StrSequence = (
                        [params.methods]
                        if isinstance(params.methods, str)
                        else list(params.methods)
                    )
                    for method in method_list:
                        if not hasattr(subject, method):
                            raise AssertionError(
                                params.msg or f"Object missing method: {method}",
                            )
                        match getattr(subject, method):
                            case method_value if callable(method_value):
                                pass
                            case _:
                                raise AssertionError(
                                    params.msg
                                    or f"Object attribute {method} is not callable",
                                )
                if params.attr_eq is not None:
                    cls._validate_attr_eq(subject, params)

            @staticmethod
            def _validate_attr_eq(
                subject: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> None:
                """Inspect original subjects while comparing owned expectations.

                Raises:
                    AssertionError: If ``not hasattr(subject, name)``; or if ``actual !=
                        wanted``.

                """
                if params.attr_eq is None:
                    return
                for name, expected in FlextTestsUtilitiesMatchersThat._named_operands(
                    params.attr_eq,
                ):
                    if not hasattr(subject, name):
                        raise AssertionError(
                            params.msg or f"Object missing attribute: {name}",
                        )
                    actual = getattr(subject, name)
                    wanted = FlextTestsPayloadUtilities.to_match_value(
                        expected,
                    )
                    if actual != wanted:
                        raise AssertionError(
                            params.msg
                            or f"Attribute {name}: expected {wanted!r}, got {actual!r}",
                        )

            # NOTE (multi-agent, mro-wkii.17 / agent: codex): combine runtime
            # assertion with generic narrowing so all analyzers retain T.
            @staticmethod
            def not_none[T](value: T | None, *, msg: str | None = None) -> T:
                """Assert and return a non-None value without changing identity.

                Returns:
                    The resulting ``T``.

                Raises:
                    AssertionError: If ``value is None``.

                """
                if value is None:
                    raise AssertionError(msg or "Expected a non-None value")
                return value

            @staticmethod
            def instance[T](
                value: p.AttributeProbe, kind: type[T], *, msg: str | None = None
            ) -> T:
                """Assert and return ``value`` narrowed to ``kind`` without copying it.

                Returns:
                    The resulting ``T``.

                Raises:
                    AssertionError: If ``value`` is not an instance of ``kind``.

                """
                if isinstance(value, kind):
                    return value
                raise AssertionError(
                    msg or f"Expected {kind.__name__}, got {type(value).__name__}"
                )

            @classmethod
            def that[SubjectT, ExpectedT](
                cls,
                value: SubjectT,
                *,
                eq: ExpectedT
                | p.Tests.ApproxLike
                | TypeAliasType
                | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
                ne: ExpectedT
                | p.Tests.ApproxLike
                | TypeAliasType
                | c.Tests.MatcherMissing = c.Tests.MatcherMissing.OMITTED,
                where: Callable[[SubjectT], bool] | None = None,
                **kwargs: p.Tests.MatcherOption,
            ) -> None:
                """Assert native operands, defaulting bare boolean subjects to True.

                Args:
                    value: The subject to be asserted.
                    eq: Native equality operand.
                    ne: Native inequality operand.
                    where: Predicate receiving the original subject.
                    **kwargs: Closed matcher criteria validated at ingress.

                Raises:
                    AssertionError: If any of the validation rules are violated.
                    ValueError: If the native truth requires the original
                        subject and it is not provided.

                """
                if (
                    isinstance(value, bool)
                    and eq is c.Tests.MatcherMissing.OMITTED
                    and ne is c.Tests.MatcherMissing.OMITTED
                    and where is None
                    and not kwargs.keys() - {"msg"}
                ):
                    kwargs = {**kwargs, "truth": True}
                params = m.Tests.ThatParams.model_validate(kwargs)
                if params.truth is not None and (
                    eq is not c.Tests.MatcherMissing.OMITTED
                    or ne is not c.Tests.MatcherMissing.OMITTED
                    or where is not None
                ):
                    msg = "Native truth cannot be combined with value criteria"
                    raise ValueError(msg)
                if params.truth is not None:
                    cls._assert_truth(value, params)
                    return
                if eq is c.Tests.MatcherMissing.OMITTED or value == eq:
                    pass
                else:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_CONSTRAINTS_FAILED.format(value=value),
                    )
                if ne is c.Tests.MatcherMissing.OMITTED or value != ne:
                    pass
                else:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_CONSTRAINTS_FAILED.format(value=value),
                    )
                if where is not None and not where(value):
                    raise AssertionError(
                        params.msg or c.Tests.ERR_PREDICATE_FAILED.format(value=value),
                    )
                cls._validate_declared_types(value, params)
                cls._validate_attrs(value, params)
                if cls._validate_subject_only(value, params):
                    return
                subject = cls._result_subject(value, params)
                subject_payload = FlextTestsPayloadUtilities.to_payload(
                    subject,
                )
                if cls._has_scalar_validation(params):
                    FlextTestsUtilitiesMatchersTypeguards.assert_scalar_match(
                        subject_payload,
                        params,
                    )
                cls._validate_common(subject_payload, params, effective_has=params.has)
                cls._validate_sequence(subject_payload, params)
                cls._validate_mapping(subject_payload, params)
                cls._validate_deep(subject_payload, params)
                cls._validate_rule_sets(subject, subject_payload, params)

            @staticmethod
            def _assert_truth(
                value: p.AttributeProbe, params: m.Tests.ThatParams
            ) -> None:
                """Compare native truth, raising the explicitly declared message only.

                Raises:
                    AssertionError: If ``bool(value)`` differs from the declared truth.

                """
                if bool(value) is params.truth:
                    return
                raise AssertionError(
                    *next(
                        (
                            (getattr(params, field),)
                            for field in ("assertion_message", "msg")
                            if field in params.model_fields_set
                        ),
                        (),
                    )
                )

            @staticmethod
            def _validate_deep(
                subject_payload: m.Tests.Payload,
                params: m.Tests.ThatParams,
            ) -> None:
                """Apply deep constraints to the canonical owned payload.

                Raises:
                    AssertionError: If ``not match_result.matched``.

                """
                if params.deep is None:
                    return
                match_result = FlextTestsPayloadUtilities.deep_match(
                    subject_payload,
                    params.deep,
                )
                if not match_result.matched:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_DEEP_PATH_FAILED.format(
                            path=match_result.path,
                            reason=match_result.reason,
                        ),
                    )

            @staticmethod
            def _validate_rule_sets(
                subject: p.AttributeProbe,
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate path, item, attribute, and predicate rule sets.

                Raises:
                    AssertionError: If ``not params.where(native)``.

                """
                if params.paths is not None:
                    FlextTestsUtilitiesMatchersThat.apply_path_rules(
                        subject_payload,
                        params.paths,
                        inherited_msg=params.msg,
                    )
                if params.items is not None:
                    FlextTestsUtilitiesMatchersThat.apply_item_rules(
                        subject_payload,
                        params.items,
                        inherited_msg=params.msg,
                    )
                if params.attrs_match is not None:
                    FlextTestsUtilitiesMatchersThat.apply_attribute_rules(
                        subject,
                        params.attrs_match,
                        inherited_msg=params.msg,
                    )
                if params.where is not None:
                    native = FlextTestsPayloadUtilities.to_match_value(
                        subject_payload,
                    )
                    if not params.where(native):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_PREDICATE_FAILED.format(value=native),
                        )

    @staticmethod
    def _named_operands(
        value: p.Tests.Payload,
    ) -> tuple[tuple[str, p.Tests.Payload], ...]:
        """Read a mapping or one name/value pair from its owned shape.

        Returns:
            The resulting ``tuple[tuple[str, p.Tests.Payload], ...]``.

        Raises:
            ValueError: If Expected a mapping or a (name, value) tuple.

        """
        if value.kind == "mapping":
            return tuple(value.entries.items())
        if (
            value.kind == "tuple"
            and len(value.items)
            == FlextTestsUtilitiesMatchersThat._TUPLE_NAME_VALUE_PAIR_LEN
        ):
            key, expected = value.items
            if key.kind == "atom" and isinstance(key.atom, str):
                return ((key.atom, expected),)
        msg = "Expected a mapping or a (name, value) tuple"
        raise ValueError(msg)

    @staticmethod
    def _rule_kwargs[SubjectT](
        rule: m.Tests.MatchRule[SubjectT],
    ) -> Mapping[
        str,
        p.Tests.Payload
        | t.Tests.PayloadAtom
        | t.Tests.LengthSpec
        | t.RegexPattern
        | type
        | t.VariadicTuple[type]
        | None,
    ]:
        parsed = rule
        return {
            key: getattr(parsed, key)
            for key in type(parsed).model_fields
            if key != "where"
            and (key in parsed.model_fields_set or getattr(parsed, key) is not None)
        }

    @classmethod
    def _apply_rule[SubjectT](
        cls,
        subject: SubjectT,
        rule: m.Tests.MatchRule[SubjectT],
        *,
        inherited_msg: str | None = None,
    ) -> None:
        kwargs = dict(cls._rule_kwargs(rule))
        kwargs.pop("eq", None)
        kwargs.pop("ne", None)
        if inherited_msg is not None and "msg" not in kwargs:
            kwargs["msg"] = inherited_msg
        if not hasattr(cls.Tests.Matchers, "that"):
            message = "Matcher rule runner missing"
            raise AssertionError(message)
        expected_eq = (
            FlextTestsPayloadUtilities.to_match_value(rule.eq)
            if isinstance(rule.eq, m.Tests.Payload)
            else rule.eq
        )
        expected_ne = (
            FlextTestsPayloadUtilities.to_match_value(rule.ne)
            if isinstance(rule.ne, m.Tests.Payload)
            else rule.ne
        )
        cls.Tests.Matchers.that(
            subject,
            eq=expected_eq
            if "eq" in rule.model_fields_set
            else c.Tests.MatcherMissing.OMITTED,
            ne=expected_ne
            if "ne" in rule.model_fields_set
            else c.Tests.MatcherMissing.OMITTED,
            where=rule.where,
            **kwargs,
        )

    @classmethod
    def apply_path_rules(
        cls,
        subject: p.Tests.Payload,
        rules: Mapping[str, m.Tests.MatchRule],
        *,
        inherited_msg: str | None = None,
    ) -> None:
        for path, rule in rules.items():
            try:
                cls._apply_rule(
                    FlextTestsPayloadUtilities.to_match_value(
                        FlextTestsPayloadUtilities.extract_path_value(
                            subject,
                            path,
                        ),
                    ),
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Path rule '{path}' failed: {exc}",
                ) from exc

    @classmethod
    def apply_item_rules(
        cls,
        subject: p.Tests.Payload,
        rules: Sequence[m.Tests.MatchRule] | Mapping[str | int, m.Tests.MatchRule],
        *,
        inherited_msg: str | None = None,
    ) -> None:
        if subject.kind in {"atom", "mapping"}:
            raise AssertionError(inherited_msg or "Item assertions require a sequence")
        sequence_value = tuple(
            FlextTestsPayloadUtilities.to_match_value(
                item,
            )
            for item in subject.items
        )
        match rules:
            case Sequence():
                for index, rule in enumerate(rules):
                    cls._apply_rule(
                        sequence_value[index],
                        rule,
                        inherited_msg=inherited_msg,
                    )
                return
            case Mapping():
                pass
            case _:
                raise AssertionError(
                    inherited_msg
                    or "Item assertions must be a sequence or selector mapping",
                )
        for selector, rule in rules.items():
            if selector in {"*", "all"}:
                for item in sequence_value:
                    cls._apply_rule(
                        item,
                        rule,
                        inherited_msg=inherited_msg,
                    )
                continue
            target_index = (
                0
                if selector == "first"
                else -1
                if selector == "last"
                else int(selector)
            )
            cls._apply_rule(
                sequence_value[target_index],
                rule,
                inherited_msg=inherited_msg,
            )

    @classmethod
    def apply_attribute_rules(
        cls,
        subject: p.AttributeProbe,
        rules: Mapping[str, m.Tests.MatchRule[p.AttributeProbe]],
        *,
        inherited_msg: str | None = None,
    ) -> None:
        for attr_path, rule in rules.items():
            current: p.AttributeProbe = subject
            for segment in attr_path.split("."):
                if u.mapping_view(current) and segment in current:
                    current = current[segment]
                elif hasattr(current, segment):
                    current = getattr(current, segment)
                else:
                    msg = f"Object missing attribute path: {attr_path}"
                    raise AssertionError(msg)
            cls._apply_rule(
                current,
                rule,
                inherited_msg=inherited_msg,
            )


__all__: list[str] = ["FlextTestsUtilitiesMatchersThat"]
