# AUTO-GENERATED FILE — Regenerate with: make gen
"""Comparison Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._comparison_parts.comparison_part_02 import (
        FlextTestsFilesComparisonMixin as FlextTestsFilesComparisonMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".comparison_part_02": ("FlextTestsFilesComparisonMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
