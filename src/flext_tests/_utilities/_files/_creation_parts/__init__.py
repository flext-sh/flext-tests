# AUTO-GENERATED FILE — Regenerate with: make gen
"""Creation Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._creation_parts.creation_part_03 import (
        FlextTestsFilesCreationMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".creation_part_03": ("FlextTestsFilesCreationMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
