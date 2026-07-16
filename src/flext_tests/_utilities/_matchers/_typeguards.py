"""Type-guard helpers for matchers — Group A.

Static methods used internally by ``FlextTestsMatchersUtilities``. Composed
via MRO from ``flext_tests._utilities.matchers``.
"""

from __future__ import annotations

from typing import TypeIs

from flext_infra import m, p, u
from flext_tests import c, t
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsMatchersTypeGuardsMixin:
    """Type compatibility and equality-guard helpers."""

    @staticmethod
    def matches_runtime_type(
        value: p.AttributeProbe, expected_type: type | tuple[type, ...]
    ) -> bool:
        """Check runtime type compatibility using canonical parent guards."""
        if isinstance(expected_type, tuple):
            return any(u.instance_of(value, item) for item in expected_type)
        matched: bool = u.instance_of(value, expected_type)
        return matched

    @staticmethod
    def prepare_eq_ne_payloads(
        actual_payload: t.Tests.TestobjectSerializable,
        eq_value: t.Tests.MatcherKwargValue | t.Tests.TestobjectSerializable | None,
        ne_value: t.Tests.MatcherKwargValue | t.Tests.TestobjectSerializable | None,
        *,
        msg: str | None,
        default_msg: str,
    ) -> tuple[
        t.Tests.TestobjectSerializable | None, t.Tests.TestobjectSerializable | None
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
        if eq_payload is not None and not isinstance(
            eq_payload, c.Tests.MATCHER_GUARD_EQ_TYPES
        ):
            if actual_payload != eq_payload:
                raise AssertionError(msg or default_msg)
            eq_payload = None
        if ne_payload is not None and not isinstance(
            ne_payload, c.Tests.MATCHER_GUARD_EQ_TYPES
        ):
            if actual_payload == ne_payload:
                raise AssertionError(msg or default_msg)
            ne_payload = None
        return (eq_payload, ne_payload)

    # NOTE (multi-agent): general_value moved here from t.Tests typings facet
    # (declaration purity - typings must not hold runtime guard behavior; mro-i6nq.11).
    @staticmethod
    def general_value(value: t.Tests.Testobject) -> TypeIs[t.Tests.Testobject]:
        """Return True when value is a supported general test object."""
        if value is None:
            return True
        if isinstance(value, (str, int, float, bool, bytes)):
            return True
        if isinstance(value, m.BaseModel):
            return True
        return isinstance(value, (list, dict))


__all__: list[str] = ["FlextTestsMatchersTypeGuardsMixin"]
