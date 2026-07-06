# AUTO-GENERATED FILE — Regenerate with: make gen
"""Filesystem Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models._filesystem_parts.filesystem_part_02 import (
        FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".filesystem_part_02": ("FlextTestsFilesystemModelsMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
