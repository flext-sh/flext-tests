"""Assertion-raising helpers for matchers — Group B.

Static methods used internally by ``FlextTestsMatchersUtilities``.
"""

from __future__ import annotations

from collections.abc import Sized
from typing import Never

from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.constants import c
from flext_tests.protocols import p
from flext_tests.typings import t


class FlextTestsMatchersAssertionsMixin:
    """Centralized AssertionError factories with structured messages."""

    @staticmethod
    def _raise_match_assertion(
        template: str,
        *,
        msg: str | None,
        container: p.AttributeProbe,
        item: p.AttributeProbe,
    ) -> Never:
        """Raise AssertionError with ``msg`` or formatted ``template``."""
        raise AssertionError(
            msg or template.format(container=container, item=item),
        )

    @staticmethod
    def assert_len_match(
        *,
        payload: t.Tests.TestobjectSerializable,
        sized: p.AttributeProbe,
        length_spec: int | tuple[int, int],
        msg: str | None,
    ) -> None:
        """Raise AssertionError if ``payload`` length doesn't match ``length_spec``."""
        if FlextTestsPayloadUtilities.length_validate(payload, length_spec):
            return
        actual_len = len(sized) if isinstance(sized, Sized) else 0
        if isinstance(length_spec, int):
            raise AssertionError(
                msg
                or c.Tests.ERR_LEN_EXACT_FAILED.format(
                    expected=length_spec,
                    actual=actual_len,
                ),
            )
        raise AssertionError(
            msg
            or c.Tests.ERR_LEN_RANGE_FAILED.format(
                min=length_spec[0],
                max=length_spec[1],
                actual=actual_len,
            ),
        )


__all__: list[str] = ["FlextTestsMatchersAssertionsMixin"]
