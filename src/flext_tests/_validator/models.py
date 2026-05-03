"""Models for FLEXT architecture validation.

Provides shared models for all validator extensions using m patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    MutableSequence,
)
from pathlib import Path
from typing import ClassVar

from flext_tests import m, p, r, t


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
                files: t.SequenceOf[Path],
                approved_exceptions: t.MappingKV[str, t.StrSequence] | None,
                validator_name: str,
                scan_file: Callable[
                    [Path, t.MappingKV[str, t.StrSequence]],
                    t.SequenceOf[m.Tests.Violation],
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

        class ScannerMixin:
            """MRO mixin: validator classes inherit ``scan(...)`` for free.

            Each consumer declares ``_VALIDATOR_KEY`` (constants key from
            ``c.Tests.VALIDATOR_*_KEY``) and a ``_scan_file`` classmethod;
            the mixin's ``scan`` delegates to ``ScanCommon.run_scan``.
            Eliminates 22 LOC × N validators of identical scaffolding.
            """

            _VALIDATOR_KEY: ClassVar[str]

            @classmethod
            def _scan_file(
                cls,
                file_path: Path,
                approved: t.MappingKV[str, t.StrSequence],
            ) -> t.SequenceOf[m.Tests.Violation]:
                """Subclass MUST override: scan one file and yield violations."""
                raise NotImplementedError

            @classmethod
            def scan(
                cls,
                files: t.SequenceOf[Path],
                approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
            ) -> p.Result[m.Tests.ScanResult]:
                """Scan files for violations using the consumer's ``_scan_file``."""
                return FlextTestsValidatorModels.Tests.ScanCommon.run_scan(
                    files=files,
                    approved_exceptions=approved_exceptions,
                    validator_name=cls._VALIDATOR_KEY,
                    scan_file=cls._scan_file,
                )


__all__: list[str] = ["FlextTestsValidatorModels"]
