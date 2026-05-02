# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._rules_dispatch import (
        FlextTestsMatchersRulesDispatchMixin,
    )
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin,
    )

_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._assertions": ("FlextTestsMatchersAssertionsMixin",),
        "._rules_dispatch": ("FlextTestsMatchersRulesDispatchMixin",),
        "._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)

__all__: list[str] = [
    "FlextTestsMatchersAssertionsMixin",
    "FlextTestsMatchersRulesDispatchMixin",
    "FlextTestsMatchersTypeGuardsMixin",
]
