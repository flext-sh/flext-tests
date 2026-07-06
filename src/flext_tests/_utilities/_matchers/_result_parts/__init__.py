# AUTO-GENERATED FILE — Regenerate with: make gen
"""Result Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._matchers._result_parts.result_part_03 import (
        FlextTestsMatchersResultMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".result_part_03": ("FlextTestsMatchersResultMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
