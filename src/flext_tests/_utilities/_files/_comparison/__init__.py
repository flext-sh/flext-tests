# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files. Comparison package.

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

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._comparison.comparison_part_02 import (
        FlextTestsUtilitiesFilesComparison,
    )
    from flext_tests._utilities._files._comparison.parsing import (
        FlextTestsFilesComparisonParsing,
    )


__all__: tuple[str, ...] = (
    "FlextTestsFilesComparisonParsing",
    "FlextTestsUtilitiesFilesComparison",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsUtilitiesFilesComparison": ".comparison_part_02",
        "FlextTestsFilesComparisonParsing": ".parsing",
    }),
    public_exports=__all__,
)
