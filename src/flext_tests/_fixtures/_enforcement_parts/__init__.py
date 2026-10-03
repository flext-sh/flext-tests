# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures. Enforcement Parts package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement_parts.build import (
        FlextTestsEnforcementBuilder,
    )
    from flext_tests._fixtures._enforcement_parts.dispatcher import (
        FlextTestsEnforcementDispatcher,
    )
    from flext_tests._fixtures._enforcement_parts.items import FlextTestsEnforcementItem
    from flext_tests._fixtures._enforcement_parts.validators import (
        FlextTestsEnforcementValidators,
    )

__all__: tuple[str, ...] = (
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".build": ("FlextTestsEnforcementBuilder",),
            ".dispatcher": ("FlextTestsEnforcementDispatcher",),
            ".items": ("FlextTestsEnforcementItem",),
            ".validators": ("FlextTestsEnforcementValidators",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
