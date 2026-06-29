"""Parsing utilities for flext-tests Make command metadata."""

from __future__ import annotations

from flext_tests._utilities._make_parts.make_parsing_part_02 import (
    FlextTestsMakeParsingUtilitiesMixin as FlextTestsMakeParsingUtilitiesMixinPart02,
)


class FlextTestsMakeParsingUtilitiesMixin(FlextTestsMakeParsingUtilitiesMixinPart02):
    """Parse flext-command TOML headers into typed Make models."""


__all__: list[str] = ["FlextTestsMakeParsingUtilitiesMixin"]
