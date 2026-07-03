"""Result-oriented matcher helpers."""

from __future__ import annotations

from flext_tests._utilities._matchers._result_parts.result_part_03 import (
    FlextTestsMatchersResultMixin as FlextTestsMatchersResultMixinPart03,
)


class FlextTestsMatchersResultMixin(FlextTestsMatchersResultMixinPart03):
    """Result assertion helpers exposed under ``Tests.Matchers``."""


__all__: list[str] = ["FlextTestsMatchersResultMixin"]
