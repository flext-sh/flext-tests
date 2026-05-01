"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Self

from flext_core import m, u
from flext_tests import c, t


class FlextTestsValidatorModelsMixin:
    class Violation(m.Value):
        """A detected architecture violation."""

        file_path: Annotated[
            Path,
            u.Field(description="Path to the offending source file."),
        ]
        line_number: Annotated[
            int,
            u.Field(description="1-based line number of the violation."),
        ]
        rule_id: Annotated[
            str,
            u.Field(description="Stable identifier for the rule that fired."),
        ]
        severity: Annotated[
            c.Tests.ValidatorSeverity,
            u.Field(description="Severity level assigned by the rule."),
        ]
        description: Annotated[
            str,
            u.Field(description="Human-readable violation description."),
        ]
        code_snippet: Annotated[
            str,
            u.Field(description="Source excerpt surrounding the violation."),
        ] = ""

        @u.field_validator("severity", mode="before")
        @classmethod
        def _coerce_severity(
            cls,
            value: c.Tests.ValidatorSeverity | str,
        ) -> c.Tests.ValidatorSeverity:
            if isinstance(value, c.Tests.ValidatorSeverity):
                return value
            return c.Tests.ValidatorSeverity(value.upper())

        def format(self) -> str:
            """Format violation as string."""
            formatted: str = c.Tests.VALIDATOR_MSG_VIOLATION_WITH_SNIPPET.format(
                rule_id=self.rule_id,
                description=self.description,
                snippet=self.code_snippet or "(no snippet)",
            )
            return formatted

        def format_short(self) -> str:
            """Format violation as short string."""
            formatted: str = c.Tests.VALIDATOR_MSG_VIOLATION.format(
                rule_id=self.rule_id,
                file=self.file_path.name,
                line=self.line_number,
            )
            return formatted

    class ScanResult(m.Value):
        """Result of a validation scan."""

        validator_name: Annotated[
            str,
            u.Field(description="Identifier of the validator that produced the scan."),
        ]
        files_scanned: Annotated[
            int,
            u.Field(description="Count of source files inspected by the validator."),
        ]
        violations: Annotated[
            t.SequenceOf[FlextTestsValidatorModelsMixin.Violation],
            u.Field(description="All violations detected during the scan."),
        ]
        passed: Annotated[
            bool,
            u.Field(description="True when the scan found no violations."),
        ]

        @classmethod
        def create(
            cls,
            validator_name: str,
            files_scanned: int,
            violations: t.SequenceOf[FlextTestsValidatorModelsMixin.Violation],
        ) -> Self:
            """Create a ScanResult from violations."""
            return cls(
                validator_name=validator_name,
                files_scanned=files_scanned,
                violations=violations,
                passed=not violations,
            )
