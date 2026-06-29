"""Universal value matcher facade."""

from __future__ import annotations

from flext_tests._utilities._matchers._that_parts.that_part_06 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart06,
)


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart06):
    """Universal value matcher exposed under ``Tests.Matchers``."""


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
