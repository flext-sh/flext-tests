"""Extracted mixin for flext_tests."""

from __future__ import annotations

import re
from re import Pattern

from flext_tests import (
    c,
    t,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsConstantsHelpersUtilitiesMixin:
    """Helpers for testing FlextConstants."""

    @staticmethod
    def compile_pattern(pattern_attr: str) -> Pattern[str]:
        """Compile a regex pattern from FlextConstants.

        Args:
            pattern_attr: Attribute name like "Patterns.EMAIL_REGEX"

        Returns:
            r[TEntity]: Result containing created entity or error
            Compiled regex pattern

        """
        parts = pattern_attr.split(".")
        current = c
        for part in parts:
            current = getattr(current, part)
        pattern_str = str(current)
        return re.compile(pattern_str, re.IGNORECASE)

    @staticmethod
    def get_constant_by_path(path: str) -> t.Tests.TestobjectSerializable:
        """Get a constant value by dot-separated path.

        Args:
            path: Dot-separated path like "Utilities.MAX_TIMEOUT_SECONDS"

        Returns:
            r[TEntity]: Result containing created entity or error
            The constant value at the given path

        """
        parts = path.split(".")
        current = c
        for part in parts:
            current = getattr(current, part)
        return FlextTestsPayloadUtilities.to_payload(current)
