# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Matchers package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsMatchersAssertionsMixin": "._assertions",
        "FlextTestsMatchersContainmentMixin": "._containment",
        "FlextTestsMatchersImmutabilityMixin": "._immutability",
        "FlextTestsMatchersResultMixin": "._result",
        "FlextTestsMatchersScopeMixin": "._scope",
        "FlextTestsMatchersThatMixin": "._that",
        "FlextTestsMatchersTypeGuardsMixin": "._typeguards",
    }),
    public_exports=__all__,
)
