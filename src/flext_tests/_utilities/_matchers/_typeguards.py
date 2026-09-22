"""Native type, equality, and scalar guards for owned matcher payloads."""

from __future__ import annotations

from collections.abc import Sized
from typing import TYPE_CHECKING, TypeAliasType

from _pytest.python_api import ApproxBase
from flext_infra import u

from flext_tests import c, m, p

from ..payload import FlextTestsPayloadUtilities

if TYPE_CHECKING:
    from flext_core import t


class FlextTestsMatchersTypeGuardsMixin:
    """Preserve native comparison semantics at the matcher boundary."""

    @staticmethod
    def matches_runtime_type(
        value: p.AttributeProbe, expected_type: type | tuple[type, ...]
    ) -> bool:
        """Check the original subject rather than its payload envelope."""
        return isinstance(value, expected_type)

    @staticmethod
    def prepare_eq_ne_payloads(
        actual_payload: p.Tests.Payload,
        eq_value: p.Tests.Payload | ApproxBase | TypeAliasType | None,
        ne_value: p.Tests.Payload | ApproxBase | TypeAliasType | None,
        *,
        msg: str | None,
        default_msg: str,
    ) -> None:
        """Compare native values directly without JSON or envelope equality."""
        actual = FlextTestsPayloadUtilities.to_match_value(actual_payload)
        for expected, equal in ((eq_value, True), (ne_value, False)):
            if expected is None:
                continue
            operand = (
                FlextTestsPayloadUtilities.to_match_value(expected)
                if isinstance(expected, m.Tests.Payload)
                else expected
            )
            if (actual == operand) is not equal:
                raise AssertionError(msg or default_msg)

    @staticmethod
    def assert_scalar_match(
        payload: p.Tests.Payload, params: m.Tests.ThatParams | m.Tests.OkParams
    ) -> None:
        """Apply native equality then the canonical finite scalar guard."""
        native = FlextTestsPayloadUtilities.to_match_value(payload)
        message = params.msg or f"Value {native!r} did not satisfy constraints"
        FlextTestsMatchersTypeGuardsMixin.prepare_eq_ne_payloads(
            payload, params.eq, params.ne, msg=params.msg, default_msg=message
        )
        if params.none is not None and (native is None) is not params.none:
            raise AssertionError(message)
        scalar_criteria = (
            params.gt,
            params.gte,
            params.lt,
            params.lte,
            params.empty,
            params.starts,
            params.ends,
        )
        if any(value is not None for value in scalar_criteria):
            guard = m.GuardCheckSpec(
                gt=params.gt,
                gte=params.gte,
                lt=params.lt,
                lte=params.lte,
                empty=params.empty,
                starts=params.starts,
                ends=params.ends,
            )
            if isinstance(native, str | int | float | bytes) or native is None:
                matches = u.chk(native, guard)
            elif isinstance(native, Sized):
                matches = u.chk(len(native), guard)
            else:
                raise AssertionError(message)
            if not matches:
                raise AssertionError(message)
        if params.match is not None and (
            not isinstance(native, str) or params.match.search(native) is None
        ):
            raise AssertionError(
                params.msg
                or c.Tests.ERR_NOT_MATCHES.format(
                    text=native, pattern=params.match.pattern
                )
            )


__all__: list[str] = ["FlextTestsMatchersTypeGuardsMixin"]
