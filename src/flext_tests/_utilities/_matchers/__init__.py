# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._assertions": ("FlextTestsMatchersAssertionsMixin",),
        "._containment": ("FlextTestsMatchersContainmentMixin",),
        "._result": ("FlextTestsMatchersResultMixin",),
        "._rules": ("FlextTestsMatchersRulesMixin",),
        "._scope": ("FlextTestsMatchersScopeMixin",),
        "._that": ("FlextTestsMatchersThatMixin",),
        "._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
