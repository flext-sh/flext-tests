# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files. Comparison Parts package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._comparison_parts.comparison_part_02 import (
        FlextTestsFilesComparisonMixin,
    )


__all__: tuple[str, ...] = ("FlextTestsFilesComparisonMixin",)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({".comparison_part_02": ("FlextTestsFilesComparisonMixin",)}),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
