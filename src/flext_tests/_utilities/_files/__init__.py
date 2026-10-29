# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for files.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files._comparison import (
        FlextTestsUtilitiesFilesComparison,
    )
    from flext_tests._utilities._files.assertions import (
        FlextTestsUtilitiesFilesAssertions,
    )
    from flext_tests._utilities._files.contexts import FlextTestsUtilitiesFilesContexts
    from flext_tests._utilities._files.creation import FlextTestsUtilitiesFilesCreation
    from flext_tests._utilities._files.info import FlextTestsUtilitiesFilesInfo
    from flext_tests._utilities._files.lifecycle import (
        FlextTestsUtilitiesFilesLifecycle,
    )
    from flext_tests._utilities._files.reading import FlextTestsUtilitiesFilesReading
    from flext_tests._utilities._files.size import FlextTestsUtilitiesFilesSize

__all__: tuple[str, ...] = (
    "FlextTestsUtilitiesFilesSize",
    "FlextTestsUtilitiesFilesAssertions",
    "FlextTestsUtilitiesFilesComparison",
    "FlextTestsUtilitiesFilesContexts",
    "FlextTestsUtilitiesFilesCreation",
    "FlextTestsUtilitiesFilesInfo",
    "FlextTestsUtilitiesFilesLifecycle",
    "FlextTestsUtilitiesFilesReading",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsUtilitiesFilesComparison": "._comparison",
        "FlextTestsUtilitiesFilesSize": ".size",
        "FlextTestsUtilitiesFilesAssertions": ".assertions",
        "FlextTestsUtilitiesFilesContexts": ".contexts",
        "FlextTestsUtilitiesFilesCreation": ".creation",
        "FlextTestsUtilitiesFilesInfo": ".info",
        "FlextTestsUtilitiesFilesLifecycle": ".lifecycle",
        "FlextTestsUtilitiesFilesReading": ".reading",
    }),
    public_exports=__all__,
)
