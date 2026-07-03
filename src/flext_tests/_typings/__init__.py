# AUTO-GENERATED FILE — Regenerate with: make gen
"""Typings package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._typings.base import (
        FlextTestsBaseTypesMixin as FlextTestsBaseTypesMixin,
    )
    from flext_tests._typings.files import (
        FlextTestsFilesTypesMixin as FlextTestsFilesTypesMixin,
    )
    from flext_tests._typings.guards import (
        FlextTestsGuardsTypesMixin as FlextTestsGuardsTypesMixin,
    )
    from flext_tests._typings.make import (
        FlextTestsMakeTypesMixin as FlextTestsMakeTypesMixin,
    )
    from flext_tests._typings.matchers import (
        FlextTestsMatchersTypesMixin as FlextTestsMatchersTypesMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": ("FlextTestsBaseTypesMixin",),
        ".files": ("FlextTestsFilesTypesMixin",),
        ".guards": ("FlextTestsGuardsTypesMixin",),
        ".make": ("FlextTestsMakeTypesMixin",),
        ".matchers": ("FlextTestsMatchersTypesMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
