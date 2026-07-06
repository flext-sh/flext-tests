# AUTO-GENERATED FILE — Regenerate with: make gen
"""Markdown Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._validator._markdown_parts.markdown_part_02 import (
        FlextValidatorMarkdown,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".markdown_part_02": ("FlextValidatorMarkdown",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
