"""Containment checks over native projections of owned matcher payloads.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_tests import c, p
from flext_tests._utilities import FlextTestsUtilitiesPayload
from flext_tests._utilities._matchers import FlextTestsUtilitiesMatchersAssertions


class FlextTestsUtilitiesMatchersContainment:
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
        target = FlextTestsUtilitiesPayload.to_match_value(
            FlextTestsUtilitiesPayload.to_payload(
                value,
            ),
        )
        for expectation, required in ((has, True), (lacks, False)):
            if expectation is None:
                continue
            operand = FlextTestsUtilitiesPayload.to_payload(
                expectation,
            )
            items = (
                operand.items
                if operand.kind in {c.Action.LIST, "tuple"}
                else (operand,)
            )
            for item in items:
                expected = FlextTestsUtilitiesPayload.to_match_value(
                    item,
                )
                if as_str:
                    present = str(expected) in str(target)
                elif isinstance(target, p.Tests.NativeMapping):
                    present = isinstance(expected, str) and any(
                        entry[0] == expected for entry in target.items()
                    )
                elif isinstance(target, str):
                    present = str(expected) in target
                elif isinstance(target, bytes):
                    present = isinstance(expected, bytes) and expected in target
                elif isinstance(target, p.Tests.NativeSequence):
                    present = any(candidate == expected for candidate in target)
                else:
                    FlextTestsUtilitiesMatchersAssertions.raise_match_assertion(
                        c.Tests.ERR_CONTAINS_FAILED
                        if required
                        else c.Tests.ERR_LACKS_FAILED,
                        msg=msg,
                        container=target,
                        item=expected,
                    )
                if present is not required:
                    FlextTestsUtilitiesMatchersAssertions.raise_match_assertion(
                        c.Tests.ERR_CONTAINS_FAILED
                        if required
                        else c.Tests.ERR_LACKS_FAILED,
                        msg=msg,
                        container=target,
                        item=expected,
                    )


__all__: list[str] = ["FlextTestsUtilitiesMatchersContainment"]
