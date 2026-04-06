"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    computed_field,
)

from flext_core import FlextModels, r
from flext_tests.constants import c
from flext_tests.typings import t


class FlextTestsBatchModelsMixin:
    class BatchParams(FlextModels.Value):
        """Parameters for FlextTestsFiles.batch() method."""

        files: Annotated[
            (
                Mapping[str, t.Tests.TestobjectSerializable]
                | Sequence[tuple[str, t.Tests.TestobjectSerializable]]
            ),
            Field(
                description="Mapping or Sequence of files to process",
            ),
        ]
        directory: Annotated[
            Path | None,
            Field(
                default=None,
                description="Target directory for create operations",
            ),
        ]
        operation: Annotated[
            c.Tests.Operation,
            BeforeValidator(
                lambda v: c.Tests.Operation(v) if isinstance(v, str) else v
            ),
            Field(
                default=c.Tests.Operation.CREATE,
                description="Operation type: create, read, or delete",
            ),
        ]
        model: Annotated[
            type[BaseModel] | None,
            Field(
                default=None,
                description="Optional model class for read operations",
            ),
        ]
        on_error: Annotated[
            c.Tests.ErrorMode,
            BeforeValidator(
                lambda v: c.Tests.ErrorMode(v) if isinstance(v, str) else v
            ),
            Field(
                default=c.Tests.ErrorMode.COLLECT,
                description="Error handling mode: stop, skip, or collect",
            ),
        ]
        parallel: Annotated[
            bool,
            Field(
                default=False,
                description="Run operations in parallel",
            ),
        ]

    class BatchResult(FlextModels.Value):
        """Result of batch file operations."""

        succeeded: Annotated[
            int,
            Field(
                ge=0,
                description="Number of successful operations",
            ),
        ]
        failed: Annotated[
            t.NonNegativeInt,
            Field(description="Number of failed operations"),
        ]
        total: Annotated[
            t.NonNegativeInt,
            Field(description="Total number of operations"),
        ]
        results: Annotated[
            Mapping[str, r[Path | t.Tests.TestobjectSerializable]],
            Field(
                description="Mapping of file names to operation results",
            ),
        ] = Field(default_factory=dict)
        errors: Annotated[
            t.StrMapping,
            Field(
                description="Mapping of file names to error messages",
            ),
        ] = Field(default_factory=dict)

        @computed_field
        def failure_count(self) -> int:
            """Alias for failed count."""
            return self.failed

        @computed_field
        def success_count(self) -> int:
            """Alias for succeeded count."""
            return self.succeeded

        @computed_field
        def success_rate(self) -> float:
            """Compute success rate as percentage."""
            if self.total == 0:
                return 0.0
            return (self.succeeded / self.total) * 100.0
