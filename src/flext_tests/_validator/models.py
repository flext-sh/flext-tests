"""Models for FLEXT architecture validation.

Provides shared models for all validator extensions using m patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableSequence, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_tests import c, m, p, r, t, u


class FlextTestsValidatorModels(m):
    """Models for FLEXT architecture validation - extends m.

    Uses c.Tests.Validator for constants (Severity, Rules, Defaults, Approved patterns).
    """

    class Tests(m.Tests):
        """Tests namespace — validator models live here."""

        class ScanCommon(m.Value):
            """Shared routines to build ScanResult payloads."""

            @staticmethod
            def run_scan(
                *,
                files: Sequence[Path],
                approved_exceptions: Mapping[str, t.StrSequence] | None,
                validator_name: str,
                scan_file: Callable[
                    [Path, Mapping[str, t.StrSequence]],
                    Sequence[m.Tests.Violation],
                ],
            ) -> p.Result[m.Tests.ScanResult]:
                violations: MutableSequence[m.Tests.Violation] = []
                approved = approved_exceptions or {}
                for file_path in files:
                    violations.extend(scan_file(file_path, approved))
                return r[m.Tests.ScanResult].ok(
                    m.Tests.ScanResult.create(
                        validator_name=validator_name,
                        files_scanned=len(files),
                        violations=violations,
                    ),
                )

        class ScanConfig(m.Value):
            """Configuration for validation scan."""

            target_path: Annotated[
                Path,
                u.Field(description="Filesystem root path to scan for violations."),
            ]
            include_patterns: Annotated[
                t.StrSequence,
                u.Field(
                    description="Glob patterns defining files that should be scanned for violations.",
                    title="Include Patterns",
                    examples=[["src/**/*.py", "tests/**/*.py"]],
                ),
            ] = u.Field(
                default_factory=lambda: list(
                    c.Tests.VALIDATOR_INCLUDE_PATTERNS,
                )
            )
            exclude_patterns: Annotated[
                t.StrSequence,
                u.Field(
                    description="Glob patterns defining files that should be excluded from scan input.",
                    title="Exclude Patterns",
                    examples=[["**/__pycache__/**", "**/.venv/**"]],
                ),
            ] = u.Field(
                default_factory=lambda: list(
                    c.Tests.VALIDATOR_EXCLUDE_PATTERNS,
                )
            )
            approved_exceptions: Annotated[
                Mapping[str, t.StrSequence],
                u.Field(
                    description="Rule-to-path allowlist for known and explicitly approved exceptions.",
                    title="Approved Exceptions",
                    examples=[{"RULE_001": ["tests/fixtures/generated.py"]}],
                ),
            ] = u.Field(default_factory=lambda: MappingProxyType({}))


__all__: list[str] = ["FlextTestsValidatorModels"]
