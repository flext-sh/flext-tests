"""Models for FLEXT architecture validation.

Provides shared models for all validator extensions using FlextTestsModels patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Annotated

from flext_core import r
from pydantic import Field

from flext_tests import c
from flext_tests.models import m


class FlextValidatorModels(m):
    """Models for FLEXT architecture validation - extends FlextTestsModels.

    Uses c.Tests.Validator for constants (Severity, Rules, Defaults, Approved patterns).
    """

    Violation = m.Tests.Violation
    ScanResult = m.Tests.ScanResult

    class ScanCommon(m.Value):
        """Shared routines to build ScanResult payloads."""

        @staticmethod
        def run_scan(
            *,
            files: list[Path],
            approved_exceptions: Mapping[str, list[str]] | None,
            validator_name: str,
            scan_file: Callable[
                [Path, Mapping[str, list[str]]],
                list[m.Tests.Violation],
            ],
        ) -> r[m.Tests.ScanResult]:
            violations: list[m.Tests.Violation] = []
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

        target_path: Path
        include_patterns: Annotated[
            list[str],
            Field(
                default_factory=lambda: list(
                    c.Tests.Validator.Defaults.INCLUDE_PATTERNS,
                ),
                description="Glob patterns defining files that should be scanned for violations.",
                title="Include Patterns",
                examples=[["src/**/*.py", "tests/**/*.py"]],
            ),
        ]
        exclude_patterns: Annotated[
            list[str],
            Field(
                default_factory=lambda: list(
                    c.Tests.Validator.Defaults.EXCLUDE_PATTERNS,
                ),
                description="Glob patterns defining files that should be excluded from scan input.",
                title="Exclude Patterns",
                examples=[["**/__pycache__/**", "**/.venv/**"]],
            ),
        ]
        approved_exceptions: Annotated[
            Mapping[str, list[str]],
            Field(
                default_factory=dict,
                description="Rule-to-path allowlist for known and explicitly approved exceptions.",
                title="Approved Exceptions",
                examples=[{"RULE_001": ["tests/fixtures/generated.py"]}],
            ),
        ]


# Short alias
vm = FlextValidatorModels

__all__ = ["FlextValidatorModels", "vm"]
