# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for enforcement.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement.build import FlextTestsEnforcementBuilder
    from flext_tests._fixtures._enforcement.collector import (
        FlextTestsFixturesEnforcementCollector,
    )
    from flext_tests._fixtures._enforcement.dispatcher import (
        FlextTestsEnforcementDispatcher,
    )
    from flext_tests._fixtures._enforcement.error import (
        FlextTestsFixturesEnforcementError,
    )
    from flext_tests._fixtures._enforcement.items import FlextTestsEnforcementItem
    from flext_tests._fixtures._enforcement.validators import (
        FlextTestsEnforcementValidators,
    )

__all__: tuple[str, ...] = (
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "FlextTestsFixturesEnforcementCollector",
    "FlextTestsFixturesEnforcementError",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsEnforcementBuilder": ".build",
        "FlextTestsEnforcementDispatcher": ".dispatcher",
        "FlextTestsEnforcementItem": ".items",
        "FlextTestsEnforcementValidators": ".validators",
        "FlextTestsFixturesEnforcementCollector": ".collector",
        "FlextTestsFixturesEnforcementError": ".error",
    }),
    public_exports=__all__,
)
