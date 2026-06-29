"""Public type validator facade for flext-tests."""

from __future__ import annotations

from flext_tests._validator._types_parts.types_part_02 import (
    FlextValidatorTypes as FlextValidatorTypesPart02,
)


class FlextValidatorTypes(FlextValidatorTypesPart02):
    """Type validation facade for FlextTestsValidator."""


__all__: list[str] = ["FlextValidatorTypes"]
