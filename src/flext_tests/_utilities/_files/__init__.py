# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsFilesAssertionsMixin": "._assertions",
        "FlextTestsFilesBatchMixin": "._batch",
        "FlextTestsFilesComparisonMixin": "._comparison",
        "FlextTestsFilesContextsMixin": "._contexts",
        "FlextTestsFilesCreationMixin": "._creation",
        "FlextTestsFilesInfoMixin": "._info",
        "FlextTestsFilesLifecycleMixin": "._lifecycle",
        "FlextTestsFilesReadingMixin": "._reading",
        "_comparison_parts": "._comparison_parts",
    }),
    public_exports=__all__,
)
