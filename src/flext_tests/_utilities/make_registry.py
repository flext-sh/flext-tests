"""Registry and contract utilities for flext-tests Make commands."""

from __future__ import annotations

from flext_tests._utilities._make_parts.make_registry_part_03 import (
    FlextTestsMakeRegistryUtilitiesMixin as FlextTestsMakeRegistryUtilitiesMixinPart03,
)


class FlextTestsMakeRegistryUtilitiesMixin(FlextTestsMakeRegistryUtilitiesMixinPart03):
    """Discover and load registry-driven Make commands."""


__all__: list[str] = ["FlextTestsMakeRegistryUtilitiesMixin"]
