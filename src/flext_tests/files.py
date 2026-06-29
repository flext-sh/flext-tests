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
from typing import ClassVar, override

from flext_tests import (
    m,
    p,
    r,
    s,
    t,
)
from flext_tests._utilities._files._comparison import FlextTestsFilesComparisonMixin
from flext_tests._utilities._files._info import FlextTestsFilesInfoMixin


class FlextTestsFiles(
    s,
    FlextTestsFilesInfoMixin,
    FlextTestsFilesComparisonMixin,
):
    """Manages test files for FLEXT ecosystem testing."""

    FileInfo: ClassVar[type[m.Tests.FileInfo]] = m.Tests.FileInfo

    def __init__(
        self,
        base_dir: Path | None = None,
    ) -> None:
        """Initialize file manager with optional base directory."""
        super().__init__()
        self._initialize_file_lifecycle(base_dir)

    @override
    def execute(self) -> p.Result[t.JsonValue]:
        """Execute service - returns success for file manager.

        FlextTestsFiles is a utility service that doesn't have a specific
        execution result. Returns success by default.
        """
        return r[t.JsonValue].ok("")


tf = FlextTestsFiles

__all__: list[str] = ["FlextTestsFiles", "tf"]
