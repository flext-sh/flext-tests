"""Universal matcher collection helpers."""

from __future__ import annotations

from collections.abc import Callable

from flext_tests._utilities._matchers._that_parts.that_part_02 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart02,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.constants import c
from flext_tests.models import m
from flext_tests.typings import t


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart02):
    """Universal matcher collection helpers."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(FlextTestsMatchersThatMixinPart02.Tests.Matchers):
            """Collection validation helpers."""

            @classmethod
            def _validate_sequence(
                cls,
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate sequence-specific predicates."""
                seq_value = cls._sequence_value(subject_payload)
                if not seq_value and not isinstance(
                    subject_payload, t.SEQUENCE_PAIR_TYPES
                ):
                    return
                cls._validate_sequence_edges(seq_value, params)
                cls._validate_sequence_quantifiers(seq_value, params)
                cls._validate_sequence_order(seq_value, params)

            @staticmethod
            def _validate_sequence_quantifiers(
                seq_value: t.SequenceOf[t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate all_/any_ sequence predicates."""
                if params.all_ is not None:
                    FlextTestsMatchersThatMixin.Tests.Matchers._validate_all(
                        seq_value,
                        params,
                    )
                if params.any_ is not None:
                    FlextTestsMatchersThatMixin.Tests.Matchers._validate_any(
                        seq_value,
                        params,
                    )

            @staticmethod
            def _validate_all(
                seq_value: t.SequenceOf[t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate that all sequence items match a predicate/type."""
                if isinstance(params.all_, type):
                    all_type = params.all_
                    if all(isinstance(item, all_type) for item in seq_value):
                        return
                    failed_idx = next(
                        (
                            index
                            for index, item in enumerate(seq_value)
                            if not isinstance(item, all_type)
                        ),
                        None,
                    )
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx),
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
                                FlextTestsPayloadUtilities.to_payload(item),
                            )
                        ),
                        None,
                    )
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_ALL_ITEMS_FAILED.format(index=failed_idx),
                    )

            @staticmethod
            def _validate_any(
                seq_value: t.SequenceOf[t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate that any sequence item matches a predicate/type."""
                if isinstance(params.any_, type):
                    any_type = params.any_
                    if not any(isinstance(item, any_type) for item in seq_value):
                        raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)
                    return
                if callable(params.any_) and not any(
                    params.any_(FlextTestsPayloadUtilities.to_payload(item))
                    for item in seq_value
                ):
                    raise AssertionError(params.msg or c.Tests.ERR_ANY_ITEMS_FAILED)

            @staticmethod
            def _validate_sequence_order(
                seq_value: t.SequenceOf[t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate sorted/unique sequence predicates."""
                sorted_param = params.sorted
                if sorted_param is not None:
                    value_list = list(seq_value)
                    if sorted_param is True:
                        sorted_list = sorted(
                            value_list,
                            key=lambda item: (type(item).__name__, str(item)),
                        )
                        if value_list != sorted_list:
                            raise AssertionError(params.msg or "Sequence is not sorted")
                    elif callable(sorted_param):
                        sorted_list = sorted(
                            value_list,
                            key=lambda item: (
                                FlextTestsMatchersThatMixin.Tests.Matchers._comparable_key(
                                    sorted_param,
                                    item,
                                )
                            ),
                        )
                        if value_list != sorted_list:
                            raise AssertionError(
                                params.msg or "Sequence is not sorted by key function",
                            )
                if (
                    params.unique is not None
                    and params.unique
                    and len(seq_value) != len(set(seq_value))
                ):
                    raise AssertionError(
                        params.msg or "Sequence contains duplicate items",
                    )

            @staticmethod
            def _comparable_key(
                user_key_fn: Callable[[t.Tests.Testobject], t.Tests.Testobject],
                item: t.Tests.TestobjectSerializable,
            ) -> t.StrPair:
                """Wrap user key to return comparable tuple."""
                result = user_key_fn(FlextTestsPayloadUtilities.to_payload(item))
                return (str(type(result).__name__), str(result))


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
