"""Universal matcher scalar and sequence helpers."""

from __future__ import annotations

from flext_infra import u
from flext_tests import c, m, t
from flext_tests._utilities._matchers._assertions import (
    FlextTestsMatchersAssertionsMixin,
)
from flext_tests._utilities._matchers._containment import (
    FlextTestsMatchersContainmentMixin,
)
from flext_tests._utilities._matchers._that_parts.that_part_01_subject import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart01Subject,
)
from flext_tests._utilities._matchers._typeguards import (
    FlextTestsMatchersTypeGuardsMixin,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart01Subject):
    """Universal matcher scalar and sequence helpers."""

    class Tests:
        class Matchers(FlextTestsMatchersThatMixinPart01Subject.Tests.Matchers):
            @staticmethod
            def _has_scalar_validation(params: m.Tests.ThatParams) -> bool:
                """Return whether scalar guard validation is requested."""
                return (
                    params.eq is not None
                    or params.ne is not None
                    or params.gt is not None
                    or params.gte is not None
                    or params.lt is not None
                    or params.lte is not None
                    or params.none is not None
                    or params.empty is not None
                    or params.starts is not None
                    or params.ends is not None
                    or params.match is not None
                )

            @classmethod
            def _validate_scalar(
                cls,
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
                raw_eq: t.Tests.MatcherKwargValue | None,
                raw_ne: t.Tests.MatcherKwargValue | None,
                kwargs: dict[str, t.Tests.MatcherKwargValue],
            ) -> None:
                """Validate scalar predicates."""
                if not cls._has_scalar_validation(params):
                    return
                chk_payload = (
                    None
                    if params.none is True and subject_payload == ""
                    else subject_payload
                )
                eq_value = raw_eq if "eq" in kwargs else params.eq
                ne_value = raw_ne if "ne" in kwargs else params.ne
                eq_payload, ne_payload = (
                    FlextTestsMatchersTypeGuardsMixin.prepare_eq_ne_payloads(
                        subject_payload,
                        eq_value,
                        ne_value,
                        msg=params.msg,
                        default_msg=(
                            f"Assertion failed: {subject_payload!r} did not satisfy constraints"
                        ),
                    )
                )
                guard = m.GuardCheckSpec.model_validate({
                    "eq": FlextTestsPayloadUtilities.to_normalized_value(eq_payload)
                    if eq_payload is not None
                    else None,
                    "ne": FlextTestsPayloadUtilities.to_normalized_value(ne_payload)
                    if ne_payload is not None
                    else None,
                    "gt": params.gt,
                    "gte": params.gte,
                    "lt": params.lt,
                    "lte": params.lte,
                    "none": params.none,
                    "empty": params.empty,
                    "starts": params.starts,
                    "ends": params.ends,
                })
                chk_plain: t.GuardInput | None = (
                    None
                    if chk_payload is None
                    else FlextTestsPayloadUtilities.to_normalized_value(chk_payload)
                )
                if not u.chk(chk_plain, guard):
                    raise AssertionError(
                        params.msg
                        or f"Assertion failed: {subject_payload!r} did not satisfy constraints"
                    )
                if (
                    params.match is not None
                    and isinstance(subject_payload, str)
                    and params.match.search(subject_payload) is None
                ):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_NOT_MATCHES.format(
                            text=subject_payload,
                            pattern=params.match.pattern,
                        ),
                    )

            @staticmethod
            def _validate_common(
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
                *,
                effective_has: t.Tests.MatcherKwargValue | None,
            ) -> None:
                """Validate containment and length predicates."""
                FlextTestsMatchersContainmentMixin.check_has_lacks(
                    subject_payload,
                    effective_has,
                    params.lacks,
                    params.msg,
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
                subject_payload: t.Tests.TestobjectSerializable,
            ) -> t.SequenceOf[t.Tests.TestobjectSerializable]:
                """Validate and normalize a sequence payload."""
                if not isinstance(subject_payload, t.SEQUENCE_PAIR_TYPES):
                    return ()
                try:
                    return t.Tests.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER.validate_python(
                        subject_payload,
                    )
                except c.ValidationError:
                    return ()

            @staticmethod
            def _validate_sequence_edges(
                seq_value: t.SequenceOf[t.Tests.TestobjectSerializable],
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate first/last sequence predicates."""
                if params.first is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check first"
                        )
                    if seq_value[0] != params.first:
                        raise AssertionError(
                            params.msg
                            or f"First item: expected {params.first!r}, got {seq_value[0]!r}",
                        )
                if params.last is not None:
                    if not seq_value:
                        raise AssertionError(
                            params.msg or "Sequence is empty, cannot check last"
                        )
                    if seq_value[-1] != params.last:
                        raise AssertionError(
                            params.msg
                            or f"Last item: expected {params.last!r}, got {seq_value[-1]!r}",
                        )


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
