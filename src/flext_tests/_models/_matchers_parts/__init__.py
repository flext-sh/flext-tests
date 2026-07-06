# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models._matchers_parts.matchers_part_03 import (
        FlextTestsMatchersModelsMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".matchers_part_03": ("FlextTestsMatchersModelsMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
