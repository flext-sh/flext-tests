"""Universal matcher mapping and attribute helpers."""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests._utilities._matchers._that_parts.that_part_03 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart03,
)
from flext_tests.constants import c
from flext_tests.models import m
from flext_tests.protocols import p
from flext_tests.typings import t


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart03):
    """Universal matcher mapping and attribute helpers."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(FlextTestsMatchersThatMixinPart03.Tests.Matchers):
            """Mapping, attribute, and deep validation helpers."""

            @staticmethod
            def _mapping_value(
                subject_payload: t.Tests.TestobjectSerializable,
            ) -> t.MappingKV[str, t.Tests.TestobjectSerializable]:
                """Validate and normalize a mapping payload."""
                if not isinstance(subject_payload, Mapping):
                    return dict[str, t.Tests.TestobjectSerializable]()
                try:
                    return (
                        t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                            subject_payload,
                        )
                    )
                except c.ValidationError:
                    return dict[str, t.Tests.TestobjectSerializable]()

            @staticmethod
            def _validate_mapping(
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate mapping-specific predicates."""
                mapping_value = (
                    FlextTestsMatchersThatMixin.Tests.Matchers._mapping_value(
                        subject_payload
                    )
                )
                if not mapping_value and not isinstance(subject_payload, Mapping):
                    return
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
                    value_list = list(mapping_value.values())
                    for expected_val in params.values:
                        if expected_val not in value_list:
                            raise AssertionError(
                                params.msg
                                or f"Expected value {expected_val!r} not found in mapping",
                            )
                if params.kv is not None:
                    FlextTestsMatchersThatMixin.Tests.Matchers._validate_kv(
                        mapping_value,
                        params,
                    )

            @staticmethod
            def _validate_kv(
                mapping_value: t.MappingKV[str, t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate key-value mapping predicates."""
                kv_items: t.SequenceOf[tuple[p.AttributeProbe, p.AttributeProbe]] = ()
                match params.kv:
                    case tuple() as key_value if len(key_value) == 2:
                        key, expected_val = key_value
                        kv_items = ((key, expected_val),)
                    case Mapping() as mapping_kv:
                        kv_items = tuple(mapping_kv.items())
                    case _:
                        kv_items = ()
                for key, expected_val in kv_items:
                    if not isinstance(key, str):
                        raise AssertionError(
                            params.msg
                            or f"Mapping key must be str, got {type(key).__name__}",
                        )
                    if key not in mapping_value:
                        raise AssertionError(
                            params.msg or f"Key {key!r} not found in mapping"
                        )
                    actual_obj = mapping_value[key]
                    if actual_obj != expected_val:
                        raise AssertionError(
                            params.msg
                            or f"Key {key!r}: expected {expected_val!r}, got {actual_obj!r}",
                        )

            @staticmethod
            def _validate_attrs(
                subject: p.AttributeProbe, params: m.Tests.ThatParams
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
                        if not callable(getattr(subject, method)):
                            raise AssertionError(
                                params.msg
                                or f"Object attribute {method} is not callable",
                            )
                if params.attr_eq is not None:
                    FlextTestsMatchersThatMixin.Tests.Matchers._validate_attr_eq(
                        subject,
                        params,
                    )

            @staticmethod
            def _validate_attr_eq(
                subject: p.AttributeProbe, params: m.Tests.ThatParams
            ) -> None:
                """Validate attribute equality predicates."""
                attr_items: t.SequenceOf[tuple[p.AttributeProbe, p.AttributeProbe]] = ()
                match params.attr_eq:
                    case tuple() as attr_spec if len(attr_spec) == 2:
                        attr, expected_val = attr_spec
                        attr_items = ((attr, expected_val),)
                    case Mapping() as attr_mapping:
                        attr_items = tuple(attr_mapping.items())
                    case _:
                        attr_items = ()
                for attr, expected_val in attr_items:
                    if not isinstance(attr, str):
                        raise AssertionError(
                            params.msg
                            or f"Attribute name must be str, got {type(attr).__name__}",
                        )
                    if not hasattr(subject, attr):
                        raise AssertionError(
                            params.msg or f"Object missing attribute: {attr}"
                        )
                    actual_val = getattr(subject, attr)
                    if actual_val != expected_val:
                        raise AssertionError(
                            params.msg
                            or f"Attribute {attr}: expected {expected_val!r}, got {actual_val!r}",
                        )


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
