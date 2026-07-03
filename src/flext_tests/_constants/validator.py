"""Public validator constants facade for flext-tests."""

from __future__ import annotations

from flext_tests._constants._validator_parts.validator_part_03 import (
    FlextTestsConstantsValidator as FlextTestsConstantsValidatorPart03,
)


class FlextTestsConstantsValidator(FlextTestsConstantsValidatorPart03):
    """Architecture validator constants facade."""


__all__: list[str] = ["FlextTestsConstantsValidator"]
