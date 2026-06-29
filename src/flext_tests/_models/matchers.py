"""Public matcher models facade for flext-tests."""

from __future__ import annotations

from flext_tests._models._matchers_parts.matchers_part_03 import (
    FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixinPart03,
)


class FlextTestsMatchersModelsMixin(FlextTestsMatchersModelsMixinPart03):
    """Matcher models facade for flext-tests."""


__all__: list[str] = ["FlextTestsMatchersModelsMixin"]
