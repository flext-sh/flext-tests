"""Containment checks over native projections of owned matcher payloads."""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests import c

from ..payload import FlextTestsPayloadUtilities
from ._assertions import FlextTestsMatchersAssertionsMixin


class FlextTestsMatchersContainmentMixin:
    """Shared has/lacks checks with preserved model and binary leaves."""

    @staticmethod
    def check_has_lacks(
        value: object,
        has: object | None,
        lacks: object | None,
        msg: str | None,
        *,
        as_str: bool = False,
    ) -> None:
        """Validate containment without converting native values to text."""
        target = FlextTestsPayloadUtilities.to_match_value(
            FlextTestsPayloadUtilities.to_payload(value)
        )
        for expectation, required in ((has, True), (lacks, False)):
            if expectation is None:
                continue
            operand = FlextTestsPayloadUtilities.to_payload(expectation)
            items = operand.items if operand.kind in {"list", "tuple"} else (operand,)
            for item in items:
                expected = FlextTestsPayloadUtilities.to_match_value(item)
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
