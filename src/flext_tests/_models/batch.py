"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated

from flext_core import FlextModels, m, p, u
from flext_tests import c, t


class FlextTestsBatchModelsMixin:
    class BatchParams(FlextModels.Value):
        """Parameters for FlextTestsFiles.batch() method."""

        files: Annotated[
            (
                Mapping[str, t.Tests.TestobjectSerializable]
                | Sequence[tuple[str, t.Tests.TestobjectSerializable]]
            ),
            m.Field(
                description="Mapping or Sequence of files to process",
            ),
        ]
        directory: Annotated[
            Path | None,
            m.Field(
                description="Target directory for create operations",
            ),
        ] = None
        operation: Annotated[
            c.Tests.Operation,
            m.BeforeValidator(
                lambda v: c.Tests.Operation(v) if isinstance(v, str) else v
            ),
            m.Field(
                default=c.Tests.Operation.CREATE,
                description="Operation type: create, read, or delete",
            ),
        ]
        model: Annotated[
            type[m.BaseModel] | None,
            m.Field(
                description="Optional model class for read operations",
            ),
        ] = None
        on_error: Annotated[
            c.Tests.ErrorMode,
            m.BeforeValidator(
                lambda v: c.Tests.ErrorMode(v) if isinstance(v, str) else v
            ),
            m.Field(
                default=c.Tests.ErrorMode.COLLECT,
                description="Error handling mode: stop, skip, or collect",
            ),
        ]
        parallel: Annotated[
            bool,
            m.Field(
                description="Run operations in parallel",
            ),
        ] = False

    class BatchResult(FlextModels.Value):
        """Result of batch file operations."""

        succeeded: Annotated[
            int,
            m.Field(
                ge=0,
                description="Number of successful operations",
            ),
        ]
        failed: Annotated[
            t.NonNegativeInt,
            m.Field(description="Number of failed operations"),
        ]
        total: Annotated[
            t.NonNegativeInt,
            m.Field(description="Total number of operations"),
        ]
        results: Annotated[
            Mapping[str, p.ResultLike[t.Tests.TestResultValue]],
            m.Field(
                description="Mapping of file names to operation results",
            ),
        ] = m.Field(default_factory=dict)
        errors: Annotated[
            t.StrMapping,
            m.Field(
                description="Mapping of file names to error messages",
            ),
        ] = m.Field(default_factory=dict)

        @u.computed_field()
        @property
        def failure_count(self) -> int:
            """Alias for failed count."""
            return self.failed

        @u.computed_field()
        @property
        def success_count(self) -> int:
            """Alias for succeeded count."""
            return self.succeeded

        @u.computed_field()
        @property
        def success_rate(self) -> float:
            """Compute success rate as percentage."""
            if self.total == 0:
                return 0.0
            return (self.succeeded / self.total) * 100.0
