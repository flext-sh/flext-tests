# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._typings.base import FlextTestsBaseTypesMixin
    from flext_tests._typings.files import FlextTestsFilesTypesMixin
    from flext_tests._typings.guards import FlextTestsGuardsTypesMixin
    from flext_tests._typings.make import FlextTestsMakeTypesMixin
    from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin


__all__: tuple[str, ...] = (
    "FlextTestsBaseTypesMixin",
    "FlextTestsFilesTypesMixin",
    "FlextTestsGuardsTypesMixin",
    "FlextTestsMakeTypesMixin",
    "FlextTestsMatchersTypesMixin",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextTestsBaseTypesMixin",),
            ".files": ("FlextTestsFilesTypesMixin",),
            ".guards": ("FlextTestsGuardsTypesMixin",),
            ".make": ("FlextTestsMakeTypesMixin",),
            ".matchers": ("FlextTestsMatchersTypesMixin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
