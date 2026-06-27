"""Rule-application helpers for matchers (deprecated alias).

Redirected to ``FlextTestsMatchersThatMixin`` to avoid circular imports
while preserving the old import path.
"""

from __future__ import annotations

from flext_tests._utilities._matchers._that import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersRulesMixin,
)

__all__: list[str] = ["FlextTestsMatchersRulesMixin"]
