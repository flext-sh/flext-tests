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
    from flext_tests._typings.base import FlextTestsTypesBase
    from flext_tests._typings.docker import FlextTestsTypesDocker
    from flext_tests._typings.files import FlextTestsTypesFiles
    from flext_tests._typings.matchers import FlextTestsTypesMatchers
    from flext_tests._typings.pytest_surface import FlextTestsTypesPytest


__all__: tuple[str, ...] = (
    "FlextTestsTypesBase",
    "FlextTestsTypesDocker",
    "FlextTestsTypesFiles",
    "FlextTestsTypesMatchers",
    "FlextTestsTypesPytest",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsTypesBase": ".base",
        "FlextTestsTypesDocker": ".docker",
        "FlextTestsTypesFiles": ".files",
        "FlextTestsTypesMatchers": ".matchers",
        "FlextTestsTypesPytest": ".pytest_surface",
    }),
    public_exports=__all__,
)
