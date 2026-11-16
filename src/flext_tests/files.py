"""File management utilities for FLEXT ecosystem tests.

Provides comprehensive file operations for testing across the FLEXT ecosystem
with a simplified API using generalist methods with powerful optional parameters.

Supports:
- r: Automatically extracts value before serialization
- Pydantic models: Serializes to JSON/YAML via model_dump()
- Lists, dicts, Mappings: Proper JSON/YAML serialization
- Generic type loading: Load files directly into Pydantic models

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Annotated, ClassVar, Self, override

from flext_tests import m, p, r, s
from flext_tests._utilities import FlextTestsUtilitiesFiles
from flext_tests._utilities._files import FlextTestsUtilitiesFilesComparison


class FlextTestsFiles(
    s,
    FlextTestsUtilitiesFiles,
    FlextTestsUtilitiesFilesComparison,
):
    """Manages test files for FLEXT ecosystem testing."""

    FileInfo: ClassVar[type[p.Tests.FileInfo]] = m.Tests.FileInfo
    base_dir: Annotated[
        Path | None,
        m.BeforeValidator(
            lambda value: Path(value) if isinstance(value, str) else value,
        ),
    ] = m.Field(default=None, description="Base directory used for file operations.")

    _created_files: list[Path] = m.PrivateAttr(default_factory=list[Path])
    _created_dirs: list[Path] = m.PrivateAttr(default_factory=list[Path])

    def __enter__(self) -> Self:
        """Context manager entry.

        Returns:
            The resulting ``Self``.

        """
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit with cleanup."""
        self.cleanup()

    @classmethod
    @override
    def _create_file_manager(cls, base_dir: Path | None) -> Self:
        """Construct a validated file manager for class-level contexts.

        Returns:
            The resulting ``Self``.

        """
        return cls(base_dir=base_dir)

    @override
    def execute(self) -> p.Result[p.Base]:
        """Execute is not the file-manager API surface.

        FlextTestsFiles is a utility service whose real API is its file
        methods (create, compare, info, ...); execute has no domain result.

        Returns:
            The resulting ``p.Result[p.Base]``.

        """
        return r[p.Base].fail(
            "Use specific file methods: create, compare, read, info, ...",
        )


tf: type[FlextTestsFiles] = FlextTestsFiles
"""File manager facade alias for flext_tests."""

__all__: list[str] = ["FlextTestsFiles", "tf"]
