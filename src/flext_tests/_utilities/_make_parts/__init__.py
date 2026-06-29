# AUTO-GENERATED FILE — Regenerate with: make gen
"""Make Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".make_contract_part_02": ("FlextTestsMakeContractUtilitiesMixin",),
        ".make_parsing_part_02": ("FlextTestsMakeParsingUtilitiesMixin",),
        ".make_registry_part_03": ("FlextTestsMakeRegistryUtilitiesMixin",),
        ".make_rendering_part_02": ("FlextTestsMakeRenderingUtilitiesMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
