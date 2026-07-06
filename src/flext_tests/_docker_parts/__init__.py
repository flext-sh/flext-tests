# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docker Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._docker_parts.docker_part_06 import (
        FlextTestsDocker as FlextTestsDocker,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".docker_part_06": ("FlextTestsDocker",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
