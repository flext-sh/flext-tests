# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files. Comparison package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._comparison.comparison_parsing import (
        FlextTestsFilesComparisonParsing,
    )
    from flext_tests._utilities._files._comparison.comparison_part_02 import (
        FlextTestsFilesComparison,
    )


__all__: tuple[str, ...] = (
    "FlextTestsFilesComparison",
    "FlextTestsFilesComparisonParsing",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsFilesComparison": ".comparison_part_02",
        "FlextTestsFilesComparisonParsing": ".comparison_parsing",
    }),
    public_exports=__all__,
)
