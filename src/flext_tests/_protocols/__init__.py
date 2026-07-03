# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._protocols.valuefactory import (
        FlextTestsValueFactoryProtocolsMixin as FlextTestsValueFactoryProtocolsMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".valuefactory": ("FlextTestsValueFactoryProtocolsMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
