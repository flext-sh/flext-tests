# AUTO-GENERATED FILE — Regenerate with: make gen
"""Validator Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._constants._validator_parts.validator_part_03 import (
        FlextTestsConstantsValidator,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".validator_part_03": ("FlextTestsConstantsValidator",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
