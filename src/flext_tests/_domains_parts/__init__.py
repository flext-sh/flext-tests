# AUTO-GENERATED FILE — Regenerate with: make gen
"""Domains Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._domains_parts.domains_part_03 import (
        FlextTestsDomains as FlextTestsDomains,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".domains_part_03": ("FlextTestsDomains",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
