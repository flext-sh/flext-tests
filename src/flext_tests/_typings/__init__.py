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
    from flext_tests._typings.docker import FlextTestsDockerTypesMixin
    from flext_tests._typings.files import FlextTestsFilesTypesMixin
    from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin
    from flext_tests._typings.pytest_surface import FlextTestsPytestTypesMixin


__all__: tuple[str, ...] = (
    "FlextTestsBaseTypesMixin",
    "FlextTestsDockerTypesMixin",
    "FlextTestsFilesTypesMixin",
    "FlextTestsMatchersTypesMixin",
    "FlextTestsPytestTypesMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsBaseTypesMixin": ".base",
        "FlextTestsDockerTypesMixin": ".docker",
        "FlextTestsFilesTypesMixin": ".files",
        "FlextTestsMatchersTypesMixin": ".matchers",
        "FlextTestsPytestTypesMixin": ".pytest_surface",
    }),
    public_exports=__all__,
)
