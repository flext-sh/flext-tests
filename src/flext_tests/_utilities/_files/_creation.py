"""File-creation helpers for FlextTestsFiles."""

from __future__ import annotations

from flext_tests._utilities._files._creation_parts.creation_part_03 import (
    FlextTestsFilesCreationMixin as FlextTestsFilesCreationMixinPart03,
)


class FlextTestsFilesCreationMixin(FlextTestsFilesCreationMixinPart03):
    """Create test files with auto-detected or explicit formats."""


__all__: list[str] = ["FlextTestsFilesCreationMixin"]
