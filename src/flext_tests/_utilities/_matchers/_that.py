"""Universal 'that' matcher utilities for flext-tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from flext_core import r
from flext_tests import c, m, p, t

from ..payload import FlextTestsPayloadUtilities
from ._assertions import FlextTestsMatchersAssertionsMixin
from ._containment import FlextTestsMatchersContainmentMixin
from ._typeguards import FlextTestsMatchersTypeGuardsMixin


class FlextTestsMatchersThatMixin:
    """Fluent matcher assertions."""

    _TUPLE_NAME_VALUE_PAIR_LEN: int = 2

    class Tests:
        """Test utility namespace."""

        class Matchers:
            """Matcher assertion helpers."""

            @staticmethod
            def _that_params(
                kwargs: Mapping[str, p.AttributeProbe],
            ) -> m.Tests.ThatParams:
                """Parse all criteria once; invalid operands are never discarded."""
                return m.Tests.ThatParams.model_validate(kwargs)

            @classmethod
            def _validate_declared_types(
                cls, value: p.AttributeProbe, params: m.Tests.ThatParams
            ) -> None:
                """Validate ``is_`` and ``not_`` against the original value."""
                value_type_name = type(value).__name__
                if params.is_ is not None:
                    cls._validate_is_type(value, params, value_type_name)
                if params.not_ is not None:
                    not_types = (
                        params.not_
                        if isinstance(params.not_, tuple)
                        else (params.not_,)
                    )
                    if any(
                        FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                            value, forbidden_type
                        )
                        for forbidden_type in not_types
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_TYPE_FAILED.format(
                                expected=f"not {params.not_}", actual=value_type_name
                            )
                        )

            @staticmethod
            def _validate_is_type(
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
                value_type_name: str,
            ) -> None:
                """Validate ``is_`` including FLEXT wrapper/model shortcuts."""
                is_types = (
                    params.is_ if isinstance(params.is_, tuple) else (params.is_,)
                )
                expected_types = tuple(
                    item for item in is_types if isinstance(item, type)
                )
                root_value = getattr(value, "root", None)
                is_mapping_wrapper = (
                    dict in expected_types
                    and isinstance(root_value, dict)
                    and value.__class__.__name__ == "Dict"
                )
                is_model_mapping = (
                    dict in expected_types
                    and isinstance(value, m.BaseModel)
                    and not isinstance(value, m.RootModel)
                )
                is_sequence_wrapper = (
                    list in expected_types
                    and isinstance(root_value, t.SEQUENCE_PAIR_TYPES)
                    and value_type_name == "ObjectList"
                )
                matches_declared_type = any(
                    FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                        value, expected_type
                    )
                    for expected_type in expected_types
                )
                if (
                    matches_declared_type
                    or is_mapping_wrapper
                    or is_model_mapping
                    or is_sequence_wrapper
                ):
                    return
                type_error = c.Tests.ERR_TYPE_FAILED.format(
                    expected=params.is_, actual=value_type_name
                )
                raise AssertionError(params.msg or f"Assertion failed: {type_error}")

            @staticmethod
            def _is_type_only(params: m.Tests.ThatParams) -> bool:
                """Recognize checks that do not require a native payload."""
                subject_fields = {
                    "msg",
                    "is_",
                    "not_",
                    "attrs",
                    "methods",
                    "attr_eq",
                    "attrs_match",
                }
                return all(
                    getattr(params, name) is None
                    for name in type(params).model_fields
                    if name not in subject_fields
                )

            @classmethod
            def _result_subject[SubjectT](
                cls, subject: SubjectT, params: m.Tests.ThatParams
            ) -> SubjectT | p.Tests.Payload:
                """Return the value to validate after result-aware unwrapping."""
                if not isinstance(subject, r):
                    return subject
                result_obj = subject
                if params.ok is not None:
                    return FlextTestsPayloadUtilities.to_payload(
                        cls._ok_value(result_obj, params)
                    )
                if params.has is not None:
                    err = result_obj.error or ""
                    FlextTestsMatchersContainmentMixin.check_has_lacks(
                        err, params.has, None, params.msg, as_str=True
                    )
                    return FlextTestsPayloadUtilities.to_payload(err)
                if result_obj.success:
                    return FlextTestsPayloadUtilities.to_payload(result_obj.value)
                raise AssertionError(
                    params.msg or c.Tests.ERR_OK_FAILED.format(error=result_obj.error)
                )

            @staticmethod
            def _ok_value[ValueT](
                result_obj: p.Result[ValueT], params: m.Tests.ThatParams
            ) -> ValueT | str:
                """Validate result ok/fail expectation and return success value."""
                if params.ok and not result_obj.success:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_OK_FAILED.format(error=result_obj.error)
                    )
                if not params.ok and result_obj.success:
                    value_str = str(result_obj.value)
                    raise AssertionError(
                        params.msg or c.Tests.ERR_FAIL_EXPECTED.format(value=value_str)
                    )
                return getattr(result_obj, "value", "") if result_obj.success else ""

            @staticmethod
            def _has_scalar_validation(params: m.Tests.ThatParams) -> bool:
                """Return whether scalar guard validation is requested."""
                return any(
                    getattr(params, name) is not None
                    for name in (
                        "eq",
                        "ne",
                        "gt",
                        "gte",
                        "lt",
                        "lte",
                        "none",
                        "empty",
                        "starts",
                        "ends",
                        "match",
                    )
                )

            @classmethod
            def _validate_scalar(
                cls, subject_payload: p.Tests.Payload, params: m.Tests.ThatParams
            ) -> None:
                """Check owned native operands without textual serialization."""
                if cls._has_scalar_validation(params):
                    FlextTestsMatchersTypeGuardsMixin.assert_scalar_match(
                        subject_payload, params
                    )

            @staticmethod
            def _validate_common(
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
                *,
                effective_has: p.Tests.Payload | None,
            ) -> None:
                """Validate containment and length predicates."""
                FlextTestsMatchersContainmentMixin.check_has_lacks(
                    subject_payload, effective_has, params.lacks, params.msg
                )
                if params.len is not None:
                    FlextTestsMatchersAssertionsMixin.assert_len_match(
                        payload=subject_payload,
                        sized=subject_payload,
                        length_spec=params.len,
                        msg=params.msg,
                    )

            @staticmethod
            def _sequence_value(
                subject_payload: p.Tests.Payload,
            ) -> t.SequenceOf[p.Tests.Payload]:
                """Read already-validated collection children."""
                return subject_payload.items

            @staticmethod
            def _validate_sequence_edges(
                seq_value: t.SequenceOf[p.Tests.Payload], params: m.Tests.ThatParams
            ) -> None:
                """Validate first/last sequence predicates."""
                if params.first is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check first"
                        )
                    if FlextTestsPayloadUtilities.to_match_value(
                        seq_value[0]
                    ) != FlextTestsPayloadUtilities.to_match_value(params.first):
                        raise AssertionError(
                            params.msg
                            or (
                                f"First item: expected {params.first!r}, "
                                f"got {seq_value[0]!r}"
                            )
                        )
                if params.last is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check last"
                        )
                    if FlextTestsPayloadUtilities.to_match_value(
                        seq_value[-1]
                    ) != FlextTestsPayloadUtilities.to_match_value(params.last):
                        raise AssertionError(
                            params.msg
                            or (
                                f"Last item: expected {params.last!r}, "
                                f"got {seq_value[-1]!r}"
                            )
                        )

            @classmethod
            def _validate_sequence(
                cls, subject_payload: p.Tests.Payload, params: m.Tests.ThatParams
            ) -> None:
                """Validate sequence-specific predicates."""
                seq_value = cls._sequence_value(subject_payload)
                if subject_payload.kind in {"atom", "mapping"}:
                    return
                cls._validate_sequence_edges(seq_value, params)
                cls._validate_sequence_quantifiers(seq_value, params)
                cls._validate_sequence_order(seq_value, params)

            @classmethod
            def _validate_sequence_quantifiers(
                cls,
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate all_/any_ sequence predicates."""
                if params.all_ is not None:
                    cls._validate_all(seq_value, params)
                if params.any_ is not None:
                    cls._validate_any(seq_value, params)

            @staticmethod
            def _validate_all(
                seq_value: t.SequenceOf[p.Tests.Payload], params: m.Tests.ThatParams
            ) -> None:
                """Validate that all sequence items match a predicate/type."""
                if isinstance(params.all_, type):
                    all_type = params.all_
                    if all(
                        isinstance(
                            FlextTestsPayloadUtilities.to_match_value(item), all_type
                        )
                        for item in seq_value
                    ):
                        return
                    failed_idx = next(
                        (
                            index
                            for index, item in enumerate(seq_value)
                            if not isinstance(
                                FlextTestsPayloadUtilities.to_match_value(item),
                                all_type,
                            )
                        ),
                        None,
                    )
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx)
                    )
                if callable(params.all_) and not all(
                    params.all_(FlextTestsPayloadUtilities.to_payload(item))
                    for item in seq_value
                ):
                    failed_idx = next(
                        (
                            index
                            for index, item in enumerate(list(seq_value))
                            if not params.all_(
                                FlextTestsPayloadUtilities.to_payload(item)
                            )
                        ),
                        None,
                    )
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx)
                    )

            @staticmethod
            def _validate_any(
                seq_value: t.SequenceOf[p.Tests.Payload], params: m.Tests.ThatParams
            ) -> None:
                """Validate that any sequence item matches a predicate/type."""
                if isinstance(params.any_, type):
                    any_type = params.any_
                    if not any(
                        isinstance(
                            FlextTestsPayloadUtilities.to_match_value(item), any_type
                        )
                        for item in seq_value
                    ):
                        raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)
                    return
                if callable(params.any_) and not any(
                    params.any_(FlextTestsPayloadUtilities.to_payload(item))
                    for item in seq_value
                ):
                    raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)

            @classmethod
            def _validate_sequence_order(
                cls,
                seq_value: t.SequenceOf[p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate sorted/unique sequence predicates."""
                sorted_param = params.sorted
                if sorted_param is not None:
                    value_list = list(seq_value)
                    if sorted_param is True:
                        sorted_list = sorted(value_list, key=cls._default_sort_key)
                        if value_list != sorted_list:
                            raise AssertionError(params.msg or "Sequence is not sorted")
                    elif callable(sorted_param):

                        def user_sort_key(item: p.Tests.Payload) -> t.StrPair:
                            return cls._comparable_key(sorted_param, item)

                        sorted_list = sorted(value_list, key=user_sort_key)
                        if value_list != sorted_list:
                            raise AssertionError(
                                params.msg or "Sequence is not sorted by key function"
                            )
                if (
                    params.unique is not None
                    and params.unique
                    and any(
                        FlextTestsPayloadUtilities.to_match_value(item)
                        == FlextTestsPayloadUtilities.to_match_value(previous)
                        for index, item in enumerate(seq_value)
                        for previous in seq_value[:index]
                    )
                ):
                    raise AssertionError(
                        params.msg or "Sequence contains duplicate items"
                    )

            @staticmethod
            def _default_sort_key(item: p.Tests.Payload) -> t.StrPair:
                """Return a deterministic key for heterogeneous matcher values."""
                native = FlextTestsPayloadUtilities.to_match_value(item)
                return type(native).__name__, str(native)

            @staticmethod
            def _comparable_key(
                user_key_fn: Callable[[p.Tests.Payload], p.Tests.Payload],
                item: p.Tests.Payload,
            ) -> t.StrPair:
                """Wrap user key to return comparable tuple."""
                result = FlextTestsPayloadUtilities.to_match_value(user_key_fn(item))
                return (type(result).__name__, str(result))

            @staticmethod
            def _mapping_value(
                subject_payload: p.Tests.Payload,
            ) -> t.MappingKV[str, p.Tests.Payload]:
                """Read already-validated mapping entries."""
                return subject_payload.entries

            @classmethod
            def _validate_mapping(
                cls, subject_payload: p.Tests.Payload, params: m.Tests.ThatParams
            ) -> None:
                """Validate mapping-specific predicates."""
                mapping_value = cls._mapping_value(subject_payload)
                if subject_payload.kind != "mapping":
                    return
                if params.keys is not None:
                    missing = set(params.keys) - set(mapping_value.keys())
                    if missing:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_KEYS_MISSING.format(keys=list(missing))
                        )
                if params.lacks_keys is not None:
                    present = set(params.lacks_keys) & set(mapping_value.keys())
                    if present:
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_KEYS_EXTRA.format(keys=list(present))
                        )
                if params.values is not None:
                    value_list = [
                        FlextTestsPayloadUtilities.to_match_value(item)
                        for item in mapping_value.values()
                    ]
                    for expected_val in params.values:
                        if (
                            FlextTestsPayloadUtilities.to_match_value(expected_val)
                            not in value_list
                        ):
                            raise AssertionError(
                                params.msg
                                or (
                                    f"Expected value {expected_val!r} "
                                    "not found in mapping"
                                )
                            )
                if params.kv is not None:
                    cls._validate_kv(mapping_value, params)

            @staticmethod
            def _validate_kv(
                mapping_value: t.MappingKV[str, p.Tests.Payload],
                params: m.Tests.ThatParams,
            ) -> None:
                """Compare owned mapping values through native projections."""
                if params.kv is None:
                    return
                for key, expected in FlextTestsMatchersThatMixin._named_operands(
                    params.kv
                ):
                    if key not in mapping_value:
                        raise AssertionError(
                            params.msg or f"Key {key!r} not found in mapping"
                        )
                    actual = FlextTestsPayloadUtilities.to_match_value(
                        mapping_value[key]
                    )
                    wanted = FlextTestsPayloadUtilities.to_match_value(expected)
                    if actual != wanted:
                        raise AssertionError(
                            params.msg
                            or f"Key {key!r}: expected {wanted!r}, got {actual!r}"
                        )

            @classmethod
            def _validate_attrs(
                cls, subject: p.AttributeProbe, params: m.Tests.ThatParams
            ) -> None:
                """Validate attrs/methods/attr_eq predicates."""
                if params.attrs is not None:
                    attr_list: t.StrSequence = (
                        [params.attrs]
                        if isinstance(params.attrs, str)
                        else list(params.attrs)
                    )
                    for attr in attr_list:
                        if not hasattr(subject, attr):
                            raise AssertionError(
                                params.msg or f"Object missing attribute: {attr}"
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
                                params.msg or f"Object missing method: {method}"
                            )
                        match getattr(subject, method):
                            case method_value if callable(method_value):
                                pass
                            case _:
                                raise AssertionError(
                                    params.msg
                                    or f"Object attribute {method} is not callable"
                                )
                if params.attr_eq is not None:
                    cls._validate_attr_eq(subject, params)

            @staticmethod
            def _validate_attr_eq(
                subject: p.AttributeProbe, params: m.Tests.ThatParams
            ) -> None:
                """Inspect original subjects while comparing owned expectations."""
                if params.attr_eq is None:
                    return
                for name, expected in FlextTestsMatchersThatMixin._named_operands(
                    params.attr_eq
                ):
                    if not hasattr(subject, name):
                        raise AssertionError(
                            params.msg or f"Object missing attribute: {name}"
                        )
                    actual = getattr(subject, name)
                    wanted = FlextTestsPayloadUtilities.to_match_value(expected)
                    if actual != wanted:
                        raise AssertionError(
                            params.msg
                            or f"Attribute {name}: expected {wanted!r}, got {actual!r}"
                        )

            # NOTE (multi-agent, mro-wkii.17 / agent: codex): combine runtime
            # assertion with generic narrowing so all analyzers retain T.
            @staticmethod
            def not_none[T](value: T | None, *, msg: str | None = None) -> T:
                """Assert and return a non-None value without changing identity."""
                if value is None:
                    raise AssertionError(msg or "Expected a non-None value")
                return value

            @classmethod
            def that(cls, value: p.AttributeProbe, **kwargs: p.AttributeProbe) -> None:
                """Assert original subjects using validated owned criteria."""
                params = cls._that_params(kwargs)
                if "eq" in kwargs and kwargs["eq"] is None and params.none is None:
                    params = params.model_copy(update={"none": True})
                if "ne" in kwargs and kwargs["ne"] is None and params.none is None:
                    params = params.model_copy(update={"none": False})
                cls._validate_declared_types(value, params)
                cls._validate_attrs(value, params)
                if cls._is_type_only(params):
                    if params.attrs_match is not None:
                        FlextTestsMatchersThatMixin.apply_attribute_rules(
                            value, params.attrs_match, inherited_msg=params.msg
                        )
                    return
                subject = cls._result_subject(value, params)
                subject_payload = FlextTestsPayloadUtilities.to_payload(subject)
                cls._validate_scalar(subject_payload, params)
                cls._validate_common(subject_payload, params, effective_has=params.has)
                cls._validate_sequence(subject_payload, params)
                cls._validate_mapping(subject_payload, params)
                cls._validate_deep(subject_payload, params)
                cls._validate_rule_sets(subject, subject_payload, params)

            @staticmethod
            def _validate_deep(
                subject_payload: m.Tests.Payload, params: m.Tests.ThatParams
            ) -> None:
                """Apply deep constraints to the canonical owned payload."""
                if params.deep is None:
                    return
                match_result = FlextTestsPayloadUtilities.deep_match(
                    subject_payload, params.deep
                )
                if not match_result.matched:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_DEEP_PATH_FAILED.format(
                            path=match_result.path, reason=match_result.reason
                        )
                    )

            @staticmethod
            def _validate_rule_sets(
                subject: p.AttributeProbe,
                subject_payload: p.Tests.Payload,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate path, item, attribute, and predicate rule sets."""
                if params.paths is not None:
                    FlextTestsMatchersThatMixin.apply_path_rules(
                        subject_payload, params.paths, inherited_msg=params.msg
                    )
                if params.items is not None:
                    FlextTestsMatchersThatMixin.apply_item_rules(
                        subject_payload, params.items, inherited_msg=params.msg
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersThatMixin.apply_attribute_rules(
                        subject, params.attrs_match, inherited_msg=params.msg
                    )
                if params.where is not None and not params.where(subject_payload):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_PREDICATE_FAILED.format(value=subject_payload)
                    )

    @staticmethod
    def _named_operands(
        value: p.Tests.Payload,
    ) -> tuple[tuple[str, p.Tests.Payload], ...]:
        """Read a mapping or one name/value pair from its owned shape."""
        if value.kind == "mapping":
            return tuple(value.entries.items())
        if (
            value.kind == "tuple"
            and len(value.items)
            == FlextTestsMatchersThatMixin._TUPLE_NAME_VALUE_PAIR_LEN
        ):
            key, expected = value.items
            if key.kind == "atom" and isinstance(key.atom, str):
                return ((key.atom, expected),)
        msg = "Expected a mapping or a (name, value) tuple"
        raise ValueError(msg)

    @staticmethod
    def _rule_kwargs(
        rule: m.Tests.MatchRule,
    ) -> Mapping[
        str,
        p.Tests.Payload
        | t.Tests.PayloadAtom
        | p.Tests.PayloadPredicate
        | t.Tests.LengthSpec
        | t.Infra.RegexPattern
        | type
        | t.VariadicTuple[type]
        | None,
    ]:
        parsed = rule
        return {
            key: getattr(parsed, key)
            for key in type(parsed).model_fields
            if key in parsed.model_fields_set or getattr(parsed, key) is not None
        }

    @classmethod
    def _apply_rule(
        cls,
        subject: p.AttributeProbe,
        rule: m.Tests.MatchRule,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        kwargs = dict(cls._rule_kwargs(rule))
        if inherited_msg is not None and "msg" not in kwargs:
            kwargs["msg"] = inherited_msg
        if not hasattr(cls.Tests.Matchers, "that"):
            message = "Matcher rule runner missing"
            raise AssertionError(message)
        cls.Tests.Matchers.that(subject, **kwargs)

    @staticmethod
    def extract_path_value(subject: p.Tests.Payload, path: str) -> p.Tests.Payload:
        """Read nested payload nodes without serializing model leaves."""
        node = subject
        for segment in path.split("."):
            if node.kind == "mapping":
                if segment not in node.entries:
                    msg = f"Path not found: {path}"
                    raise AssertionError(msg)
                node = node.entries[segment]
            elif node.kind != "atom":
                node = node.items[int(segment)]
            else:
                if not hasattr(node.atom, segment):
                    msg = f"Path not found: {path}"
                    raise AssertionError(msg)
                node = FlextTestsPayloadUtilities.to_payload(
                    getattr(node.atom, segment)
                )
        return node

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
                    cls.extract_path_value(subject, path),
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Path rule '{path}' failed: {exc}"
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
        sequence_value = subject.items
        match rules:
            case Sequence():
                for index, rule in enumerate(rules):
                    cls._apply_rule(
                        sequence_value[index], rule, inherited_msg=inherited_msg
                    )
                return
            case Mapping():
                pass
            case _:
                raise AssertionError(
                    inherited_msg
                    or "Item assertions must be a sequence or selector mapping"
                )
        for selector, rule in rules.items():
            if selector in {"*", "all"}:
                for item in sequence_value:
                    cls._apply_rule(item, rule, inherited_msg=inherited_msg)
                continue
            target_index = (
                0
                if selector == "first"
                else -1
                if selector == "last"
                else int(selector)
            )
            cls._apply_rule(
                sequence_value[target_index], rule, inherited_msg=inherited_msg
            )

    @classmethod
    def apply_attribute_rules(
        cls,
        subject: p.AttributeProbe,
        rules: Mapping[str, m.Tests.MatchRule],
        *,
        inherited_msg: str | None = None,
    ) -> None:
        for attr_path, rule in rules.items():
            current = subject
            for segment in attr_path.split("."):
                if isinstance(current, Mapping) and segment in current:
                    current = current[segment]
                elif hasattr(current, segment):
                    current = getattr(current, segment)
                else:
                    msg = f"Object missing attribute path: {attr_path}"
                    raise AssertionError(msg)
            try:
                cls._apply_rule(current, rule, inherited_msg=inherited_msg)
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Attribute rule '{attr_path}' failed: {exc}"
                ) from exc


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
