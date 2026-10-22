# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures. Enforcement package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement._collector import (
        FlextTestsEnforcementCollector,
    )
    from flext_tests._fixtures._enforcement._error import (
        FlextTestsEnforcementViolationError,
    )
    from flext_tests._fixtures._enforcement.build import FlextTestsEnforcementBuilder
    from flext_tests._fixtures._enforcement.dispatcher import (
        FlextTestsEnforcementDispatcher,
    )
    from flext_tests._fixtures._enforcement.items import FlextTestsEnforcementItem
    from flext_tests._fixtures._enforcement.validators import (
        FlextTestsEnforcementValidators,
    )


__all__: tuple[str, ...] = (
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementCollector",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "FlextTestsEnforcementViolationError",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsEnforcementBuilder": ".build",
        "FlextTestsEnforcementCollector": "._collector",
        "FlextTestsEnforcementDispatcher": ".dispatcher",
        "FlextTestsEnforcementItem": ".items",
        "FlextTestsEnforcementValidators": ".validators",
        "FlextTestsEnforcementViolationError": "._error",
    }),
    public_exports=__all__,
)
