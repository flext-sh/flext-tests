"""File-comparison helpers for FlextTestsFiles."""

from __future__ import annotations

from flext_tests._utilities._files._comparison_parts.comparison_part_02 import (
    FlextTestsFilesComparisonMixin as FlextTestsFilesComparisonMixinPart02,
)


class FlextTestsFilesComparisonMixin(FlextTestsFilesComparisonMixinPart02):
    """Compare two files by content, lines, size, hash, or deep structure."""


__all__: list[str] = ["FlextTestsFilesComparisonMixin"]
