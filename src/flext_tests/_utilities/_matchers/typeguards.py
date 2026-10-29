"""Native type, equality, and scalar guards for owned matcher payloads.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sized
from operator import ge, gt, le, lt
from typing import Final

import pytest

from flext_tests import c, m, p
from flext_tests._utilities import FlextTestsUtilitiesPayload

ApproxBase: Final[type] = type(pytest.approx(0))
"""Approximation sentinel base resolved through pytest's public ``approx`` API."""


class FlextTestsUtilitiesMatchersTypeguards:
    """Preserve native comparison semantics at the matcher boundary."""

    @staticmethod
    def _scalar_guard_matches(
        value: float | str | bytes | None,
        guard: m.GuardCheckSpec,
    ) -> bool:
        """Check one scalar against the guard spec's declared criteria.

        Returns:
            The resulting ``bool``.

        """
        native: float | str | None = (
            value.decode(c.DEFAULT_ENCODING) if isinstance(value, bytes) else value
        )
        if guard.empty is not None and (native in {None, ""}) is not guard.empty:
            return False
        if native is None:
            return guard.empty is True
        for compare, bound in (
            (gt, guard.gt),
            (ge, guard.gte),
            (lt, guard.lt),
            (le, guard.lte),
        ):
            if bound is not None and not compare(native, bound):
                return False
        if guard.starts is not None and (
            not isinstance(native, str) or not native.startswith(guard.starts)
        ):
            return False
        return not (
            guard.ends is not None
            and (not isinstance(native, str) or not native.endswith(guard.ends))
        )

    @classmethod
    def assert_scalar_match(
        cls,
        payload: p.Tests.Payload,
        params: m.Tests.ThatParams,
    ) -> None:
        """Apply the canonical finite scalar guard to the native projection.

        Raises:
            AssertionError: If ``params.none is not None and (native is None) is not
                params.none``; or if ``params.match is not None and (not
                isinstance(native, str) or params.match.search(native) is None)``; or if
                ``not matches``; or if ``not (isinstance(native, Sized))``.

        """
        native = FlextTestsUtilitiesPayload.to_match_value(
            payload,
        )
        message = params.msg or c.Tests.ERR_CONSTRAINTS_FAILED.format(value=native)
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
                matches = cls._scalar_guard_matches(native, guard)
            elif isinstance(native, Sized):
                matches = cls._scalar_guard_matches(len(native), guard)
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


__all__: list[str] = ["FlextTestsUtilitiesMatchersTypeguards"]
