"""Type-guard helpers for matchers — Group A.

Static methods used internally by ``FlextTestsMatchersUtilities``. Composed
via MRO from ``flext_tests._utilities.matchers``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flext_core.utilities import u
from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.protocols import p
from flext_tests.typings import t


class FlextTestsMatchersTypeGuardsMixin:
    """Type compatibility and equality-guard helpers."""

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
    def matches_runtime_type(
        value: p.AttributeProbe,
        expected_type: type | tuple[type, ...],
    ) -> bool:
        """Check runtime type compatibility using flext-core guards."""
        if isinstance(expected_type, tuple):
            return any(
                FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(value, item)
                for item in expected_type
            )
        return u.instance_of(value, expected_type)

    @staticmethod
    def _supports_guard_eq(
        value: t.Tests.TestobjectSerializable | None,
    ) -> bool:
        return value is None or isinstance(
            value,
            FlextTestsMatchersTypeGuardsMixin._GUARD_EQ_TYPES,
        )

    @staticmethod
    def prepare_eq_ne_payloads(
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
            and not FlextTestsMatchersTypeGuardsMixin._supports_guard_eq(
                eq_payload,
            )
        ):
            if actual_payload != eq_payload:
                raise AssertionError(msg or default_msg)
            eq_payload = None
        if (
            ne_payload is not None
            and not FlextTestsMatchersTypeGuardsMixin._supports_guard_eq(
                ne_payload,
            )
        ):
            if actual_payload == ne_payload:
                raise AssertionError(msg or default_msg)
            ne_payload = None
        return (eq_payload, ne_payload)


__all__: list[str] = ["FlextTestsMatchersTypeGuardsMixin"]
