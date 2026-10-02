# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Matchers package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._containment import (
        FlextTestsMatchersContainmentMixin,
    )
    from flext_tests._utilities._matchers._immutability import (
        FlextTestsMatchersImmutabilityMixin,
    )
    from flext_tests._utilities._matchers._result import FlextTestsMatchersResultMixin
    from flext_tests._utilities._matchers._scope import FlextTestsMatchersScopeMixin
    from flext_tests._utilities._matchers._that import FlextTestsMatchersThatMixin
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin,
    )


__all__: tuple[str, ...] = (
    "FlextTestsMatchersAssertionsMixin",
    "FlextTestsMatchersContainmentMixin",
    "FlextTestsMatchersImmutabilityMixin",
    "FlextTestsMatchersResultMixin",
    "FlextTestsMatchersScopeMixin",
    "FlextTestsMatchersThatMixin",
    "FlextTestsMatchersTypeGuardsMixin",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._containment": ("FlextTestsMatchersContainmentMixin",),
            "._immutability": ("FlextTestsMatchersImmutabilityMixin",),
            "._result": ("FlextTestsMatchersResultMixin",),
            "._scope": ("FlextTestsMatchersScopeMixin",),
            "._that": ("FlextTestsMatchersThatMixin",),
            "._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
