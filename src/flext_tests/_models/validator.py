"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from pydantic import (
    field_validator,
)

from flext_tests import c


class FlextTestsValidatorModelsMixin:
    class Violation(FlextModels.Value):
        """A detected architecture violation."""

        file_path: Path
        line_number: int
        rule_id: str
        severity: c.Tests.Validator.Severity
        description: str
        code_snippet: str = ""

        @field_validator("severity", mode="before")
        @classmethod
        def _coerce_severity(
            cls,
            value: c.Tests.Validator.Severity | str,
        ) -> c.Tests.Validator.Severity:
            if isinstance(value, c.Tests.Validator.Severity):
                return value
            return c.Tests.Validator.Severity(str(value).upper())

        def format(self) -> str:
            """Format violation as string."""
            return c.Tests.Validator.Messages.VIOLATION_WITH_SNIPPET.format(
                rule_id=self.rule_id,
                description=self.description,
                snippet=self.code_snippet or "(no snippet)",
            )

        def format_short(self) -> str:
            """Format violation as short string."""
            return c.Tests.Validator.Messages.VIOLATION.format(
                rule_id=self.rule_id,
                file=self.file_path.name,
                line=self.line_number,
            )

    class ScanResult(FlextModels.Value):
        """Result of a validation scan."""

        validator_name: str
        files_scanned: int
        violations: Sequence[FlextTestsModels.Tests.Violation]
        passed: bool

        @classmethod
        def create(
            cls,
            validator_name: str,
            files_scanned: int,
            violations: Sequence[FlextTestsModels.Tests.Violation],
        ) -> FlextTestsModels.Tests.ScanResult:
            """Create a ScanResult from violations."""
            return cls(
                validator_name=validator_name,
                files_scanned=files_scanned,
                violations=violations,
                passed=not violations,
            )
