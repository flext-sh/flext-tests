"""Extracted mixin for flext_tests."""

from __future__ import annotations

import re
from re import Pattern

from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.constants import FlextTestsConstants as c


class FlextTestsConstantsHelpersUtilitiesMixin:
    """Helpers for testing FlextConstants."""

    @staticmethod
    def compile_pattern(pattern_attr: str) -> Pattern[str]:
        """Compile a regex pattern from FlextConstants."""
        parts = pattern_attr.split(".")
        current = c
        for part in parts:
            current = getattr(current, part)
        pattern_str = str(current)
        return re.compile(pattern_str, re.IGNORECASE)

    @staticmethod
    def resolve_constant_by_path(
        path: str,
    ) -> FlextTestsBaseTypesMixin.TestobjectSerializable:
        """Get a constant value by dot-separated path."""
        parts = path.split(".")
        current = c
        for part in parts:
            current = getattr(current, part)
        return FlextTestsPayloadUtilities.to_payload(current)
