"""Native type, equality, and scalar guards for owned matcher payloads.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sized
from typing import Final, Protocol, TypeAliasType, runtime_checkable

import pytest
from flext_cli import u

from flext_tests import c, m, p
from flext_tests._utilities.payload import FlextTestsFlextUtilitiesPayload

ApproxBase: Final[type] = type(pytest.approx(0))
"""Approximation sentinel base resolved through pytest's public ``approx`` API."""


@runtime_checkable
class ApproxLike(Protocol):
    """Structural stand-in for pytest approximation objects in type positions."""


class FlextTestsMatchersTypeGuardsMixin:
    """Preserve native comparison semantics at the matcher boundary."""

    @staticmethod
    def matches_runtime_type(
        value: p.AttributeProbe,
        expected_type: type | tuple[type, ...],
        *,
        owned_payload: bool = False,
    ) -> bool:
        """Check original subjects or explicitly owned internal rule nodes.

        Returns:
            The resulting ``bool``.
        """
        if owned_payload and isinstance(value, m.Tests.Payload):
            if value.kind == "atom":
                return isinstance(value.atom, expected_type)
            return issubclass(
                c.Tests.PAYLOAD_COLLECTION_TYPES[value.kind],
                expected_type,
            )
        return isinstance(value, expected_type)

    @staticmethod
    def prepare_eq_ne_payloads(
        actual_payload: p.Tests.Payload,
        eq_value: p.Tests.Payload | ApproxLike | TypeAliasType | None,
        ne_value: p.Tests.Payload | ApproxLike | TypeAliasType | None,
        *,
        msg: str | None,
        default_msg: str,
    ) -> None:
        """Compare native values directly without JSON or envelope equality.

        Raises:
            AssertionError: If ``(actual == operand) is not equal``.
        """
        actual = (
            FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_match_value(
                actual_payload,
            )
        )
        for expected, equal in ((eq_value, True), (ne_value, False)):
            if expected is None:
                continue
            operand = (
                FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_match_value(
                    expected,
                )
                if isinstance(expected, m.Tests.Payload)
                else expected
            )
            if (actual == operand) is not equal:
                raise AssertionError(msg or default_msg)

    @staticmethod
    def assert_scalar_match(
        payload: p.Tests.Payload,
        params: m.Tests.ThatParams | m.Tests.OkParams,
    ) -> None:
        """Apply native equality then the canonical finite scalar guard.

        Raises:
            AssertionError: If ``params.none is not None and (native is None) is not
                params.none``; or if ``params.match is not None and (not
                isinstance(native, str) or params.match.search(native) is None)``; or if
                ``not matches``; or if ``not (isinstance(native, Sized))``.
        """
        native = (
            FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_match_value(
                payload,
            )
        )
        message = params.msg or c.Tests.ERR_CONSTRAINTS_FAILED.format(value=native)
        FlextTestsMatchersTypeGuardsMixin.prepare_eq_ne_payloads(
            payload,
            params.eq,
            params.ne,
            msg=params.msg,
            default_msg=message,
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
                    text=native,
                    pattern=params.match.pattern,
                ),
            )


__all__: list[str] = ["FlextTestsMatchersTypeGuardsMixin"]
