# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._typings.base import FlextTestsBaseTypesMixin
    from flext_tests._typings.files import FlextTestsFilesTypesMixin
    from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin


__all__: tuple[str, ...] = (
    "FlextTestsBaseTypesMixin",
    "FlextTestsFilesTypesMixin",
    "FlextTestsMatchersTypesMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsBaseTypesMixin": ".base",
        "FlextTestsFilesTypesMixin": ".files",
        "FlextTestsMatchersTypesMixin": ".matchers",
    }),
    public_exports=__all__,
)
