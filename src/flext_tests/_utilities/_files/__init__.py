# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files import _comparison_parts
    from flext_tests._utilities._files._assertions import FlextTestsFilesAssertionsMixin
    from flext_tests._utilities._files._batch import FlextTestsFilesBatchMixin
    from flext_tests._utilities._files._comparison import FlextTestsFilesComparisonMixin
    from flext_tests._utilities._files._contexts import FlextTestsFilesContextsMixin
    from flext_tests._utilities._files._creation import FlextTestsFilesCreationMixin
    from flext_tests._utilities._files._info import FlextTestsFilesInfoMixin
    from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin
    from flext_tests._utilities._files._reading import FlextTestsFilesReadingMixin


__all__: tuple[str, ...] = (
    "FlextTestsFilesAssertionsMixin",
    "FlextTestsFilesBatchMixin",
    "FlextTestsFilesComparisonMixin",
    "FlextTestsFilesContextsMixin",
    "FlextTestsFilesCreationMixin",
    "FlextTestsFilesInfoMixin",
    "FlextTestsFilesLifecycleMixin",
    "FlextTestsFilesReadingMixin",
    "_comparison_parts",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._batch": ("FlextTestsFilesBatchMixin",),
            "._comparison": ("FlextTestsFilesComparisonMixin",),
            "._comparison_parts": ("_comparison_parts",),
            "._contexts": ("FlextTestsFilesContextsMixin",),
            "._creation": ("FlextTestsFilesCreationMixin",),
            "._info": ("FlextTestsFilesInfoMixin",),
            "._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._reading": ("FlextTestsFilesReadingMixin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
