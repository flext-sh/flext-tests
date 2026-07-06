# AUTO-GENERATED FILE — Regenerate with: make gen
"""Settings Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._validator._settings_parts.settings_part_02 import (
        FlextValidatorSettings,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".settings_part_02": ("FlextValidatorSettings",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
