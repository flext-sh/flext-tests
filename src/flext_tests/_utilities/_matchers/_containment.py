"""Containment checks over native projections of owned matcher payloads.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests import c, p
from flext_tests._utilities._matchers._assertions import (
    FlextTestsMatchersAssertionsMixin,
)
from flext_tests._utilities.payload import FlextTestsFlextUtilitiesPayload


class FlextTestsMatchersContainmentMixin:
    """Shared has/lacks checks with preserved model and binary leaves."""

    @staticmethod
    def check_has_lacks(
        value: p.AttributeProbe,
        has: p.AttributeProbe | None,
        lacks: p.AttributeProbe | None,
        msg: str | None,
        *,
        as_str: bool = False,
    ) -> None:
        """Validate containment without converting native values to text."""
        target = (
            FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_match_value(
                FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_payload(
                    value,
                ),
            )
        )
        for expectation, required in ((has, True), (lacks, False)):
            if expectation is None:
                continue
            operand = (
                FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_payload(
                    expectation,
                )
            )
            items = operand.items if operand.kind in {"list", "tuple"} else (operand,)
            for item in items:
                expected = FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_match_value(
                    item,
                )
                if as_str:
                    present = str(expected) in str(target)
                elif isinstance(target, Mapping):
                    present = isinstance(expected, str) and any(
                        key == expected for key in target
                    )
                elif isinstance(target, str):
                    present = str(expected) in target
                elif isinstance(target, bytes):
                    present = isinstance(expected, bytes) and expected in target
                elif isinstance(target, list):
                    present = any(candidate == expected for candidate in target)
                else:
                    FlextTestsMatchersAssertionsMixin.raise_match_assertion(
                        c.Tests.ERR_CONTAINS_FAILED
                        if required
                        else c.Tests.ERR_LACKS_FAILED,
                        msg=msg,
                        container=target,
                        item=expected,
                    )
                if present is not required:
                    FlextTestsMatchersAssertionsMixin.raise_match_assertion(
                        c.Tests.ERR_CONTAINS_FAILED
                        if required
                        else c.Tests.ERR_LACKS_FAILED,
                        msg=msg,
                        container=target,
                        item=expected,
                    )


__all__: list[str] = ["FlextTestsMatchersContainmentMixin"]
