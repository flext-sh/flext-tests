# AUTO-GENERATED FILE — Regenerate with: make gen
"""Orchestration Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._validator._orchestration_parts.validator_part_02 import (
        FlextTestsValidator,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".validator_part_02": ("FlextTestsValidator",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
