"""Public filesystem models facade for flext-tests."""

from __future__ import annotations

from flext_tests._models._filesystem_parts.filesystem_part_02 import (
    FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixinPart02,
)


class FlextTestsFilesystemModelsMixin(FlextTestsFilesystemModelsMixinPart02):
    """Filesystem models facade for flext-tests."""


__all__: list[str] = ["FlextTestsFilesystemModelsMixin"]
