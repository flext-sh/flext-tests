"""Contract and resolver utilities for flext-tests Make commands."""

from __future__ import annotations

from flext_tests._utilities._make_parts.make_contract_part_02 import (
    FlextTestsMakeContractUtilitiesMixin as FlextTestsMakeContractUtilitiesMixinPart02,
)


class FlextTestsMakeContractUtilitiesMixin(FlextTestsMakeContractUtilitiesMixinPart02):
    """Validate command contracts and resolve registry entries."""


__all__: list[str] = ["FlextTestsMakeContractUtilitiesMixin"]
