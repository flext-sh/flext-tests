"""Immutability matcher — assignment rejection for frozen and constant surfaces.

Owns the dynamic attribute assignment that a negative immutability test performs.
Holding it here keeps the mechanism in library code, so test suites assert
immutability without spelling a constant-name assignment at every call site.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from flext_tests import p


class FlextTestsMatchersImmutabilityMixin:
    """Assignment-rejection matcher exposed under ``Tests.Matchers``."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers:
            """Test matchers with powerful generalist methods."""

            @staticmethod
            def rejects_assignment(
                target: p.AttributeProbe,
                field: str,
                value: p.AttributeProbe,
                *,
                expected: type[BaseException] | tuple[type[BaseException], ...],
                match: str | None = None,
            ) -> None:
                """Assert assigning ``value`` to ``field`` on ``target`` is rejected.

                Args:
                    target: Instance or class under test.
                    field: Attribute name the assignment targets.
                    value: Value the target must refuse.
                    expected: Exception type(s) the rejection must raise.
                    match: Optional regex the rejection message must contain.

                The rejection is asserted by ``pytest.raises``: an accepted
                assignment fails the test, a reason that does not match
                ``match`` raises ``AssertionError`` whose ``__context__`` is the
                original rejection, and exceptions outside ``expected``
                propagate unchanged.

                """
                with pytest.raises(expected, match=match):
                    setattr(target, field, value)


__all__: list[str] = ["FlextTestsMatchersImmutabilityMixin"]
