# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for matchers.

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
    from flext_tests._utilities._matchers.assertions import (
        FlextTestsUtilitiesMatchersAssertions,
    )
    from flext_tests._utilities._matchers.containment import (
        FlextTestsUtilitiesMatchersContainment,
    )
    from flext_tests._utilities._matchers.immutability import (
        FlextTestsUtilitiesMatchersImmutability,
    )
    from flext_tests._utilities._matchers.result import (
        FlextTestsUtilitiesMatchersResult,
    )
    from flext_tests._utilities._matchers.scope import FlextTestsUtilitiesMatchersScope
    from flext_tests._utilities._matchers.that import FlextTestsUtilitiesMatchersThat
    from flext_tests._utilities._matchers.typeguards import (
        FlextTestsUtilitiesMatchersTypeguards,
    )

__all__: tuple[str, ...] = (
    "FlextTestsUtilitiesMatchersAssertions",
    "FlextTestsUtilitiesMatchersContainment",
    "FlextTestsUtilitiesMatchersImmutability",
    "FlextTestsUtilitiesMatchersResult",
    "FlextTestsUtilitiesMatchersScope",
    "FlextTestsUtilitiesMatchersThat",
    "FlextTestsUtilitiesMatchersTypeguards",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsUtilitiesMatchersAssertions": ".assertions",
        "FlextTestsUtilitiesMatchersContainment": ".containment",
        "FlextTestsUtilitiesMatchersImmutability": ".immutability",
        "FlextTestsUtilitiesMatchersResult": ".result",
        "FlextTestsUtilitiesMatchersScope": ".scope",
        "FlextTestsUtilitiesMatchersThat": ".that",
        "FlextTestsUtilitiesMatchersTypeguards": ".typeguards",
    }),
    public_exports=__all__,
)
