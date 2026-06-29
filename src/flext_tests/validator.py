"""Public architecture validator facade for flext-tests."""

from __future__ import annotations

from flext_tests._validator._orchestration_parts.validator_part_02 import (
    FlextTestsValidator as FlextTestsValidatorPart02,
)


class FlextTestsValidator(FlextTestsValidatorPart02):
    """FLEXT architecture validator facade."""


tv = FlextTestsValidator
__all__: list[str] = ["FlextTestsValidator", "tv"]
