"""Markdown Python code block validation for FLEXT architecture.

Extracts Python code blocks from .md files and validates them against
project linting rules (syntax, forbidden imports, missing annotations).

Uses FlextInfraUtilitiesParsing from flext-infra for all parsing.
All constants centralized in c.Tests.VALIDATOR_*.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import TYPE_CHECKING

from flext_infra import FlextInfraUtilitiesParsing
from flext_tests import FlextTestsValidatorModels, c, p, t, u

if TYPE_CHECKING:
    from flext_tests import m


class FlextValidatorMarkdown:
    """Markdown Python code block validator.

    Validates ```python blocks in .md files via c.Tests constants
    and FlextInfraUtilitiesParsing for all code parsing.
    """

    @classmethod
    def markdown(
        cls,
        paths: Sequence[Path],
        *,
        approved_exceptions: Mapping[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate Python code blocks in markdown files."""
        return FlextTestsValidatorModels.Tests.ScanCommon.run_scan(
            files=list(paths),
            approved_exceptions=approved_exceptions,
            validator_name=c.Tests.VALIDATOR_MARKDOWN_KEY,
            scan_file=cls._scan_file,
        )

    @classmethod
    def _scan_file(
        cls,
        file_path: Path,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Scan a single markdown file for Python code block violations."""
        violations: MutableSequence[m.Tests.Violation] = []

        try:
            content = file_path.read_text(encoding=c.Tests.DEFAULT_ENCODING)
        except OSError:
            return violations

        lines = content.splitlines()

        for match in c.Tests.VALIDATOR_MD_PYTHON_BLOCK_RE.finditer(content):
            code = match.group(1)
            block_start = content[: match.start()].count("\n") + 1

            tree = FlextInfraUtilitiesParsing.parse_source_ast(code)
            if tree is None:
                violations.append(
                    u.Tests.create_violation(
                        file_path,
                        block_start,
                        "MD-001",
                        lines,
                        c.Tests.VALIDATOR_MSG_MD_SYNTAX.format(msg="invalid Python"),
                    )
                )
                continue

            cls._check_forbidden_imports(
                file_path,
                code,
                lines,
                block_start,
                approved,
                violations,
            )
            cls._check_object_annotations(
                file_path,
                code,
                lines,
                block_start,
                approved,
                violations,
            )
            cls._check_future_annotations(
                file_path,
                code,
                lines,
                block_start,
                approved,
                violations,
            )

        return violations

    @classmethod
    def _check_forbidden_imports(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        approved: Mapping[str, t.StrSequence],
        violations: MutableSequence[m.Tests.Violation],
    ) -> None:
        """Check for forbidden typing imports via line scanning."""
        if u.Tests.approved("MD-002", file_path, approved):
            return
        for line_offset, code_line in enumerate(code.splitlines()):
            stripped = code_line.strip()
            if not stripped.startswith(c.Tests.VALIDATOR_MD_TYPING_IMPORT_PREFIX):
                continue
            for name in c.Tests.VALIDATOR_MD_FORBIDDEN_TYPING_NAMES:
                if name in stripped:
                    violations.append(
                        u.Tests.create_violation(
                            file_path,
                            block_start + line_offset + 1,
                            "MD-002",
                            lines,
                            c.Tests.VALIDATOR_MSG_MD_FORBIDDEN_IMPORT.format(
                                import_name=f"from typing import {name}",
                            ),
                        )
                    )

    @classmethod
    def _check_object_annotations(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        approved: Mapping[str, t.StrSequence],
        violations: MutableSequence[m.Tests.Violation],
    ) -> None:
        """Check for 'object' used as type annotation."""
        if u.Tests.approved("MD-004", file_path, approved):
            return
        for line_offset, code_line in enumerate(code.splitlines()):
            if c.Tests.VALIDATOR_MD_OBJECT_ANNOTATION_RE.search(code_line):
                violations.append(
                    u.Tests.create_violation(
                        file_path,
                        block_start + line_offset + 1,
                        "MD-004",
                        lines,
                        c.Tests.VALIDATOR_MSG_MD_FORBIDDEN_ANNOTATION.format(
                            annotation="object",
                        ),
                    )
                )

    @classmethod
    def _check_future_annotations(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        approved: Mapping[str, t.StrSequence],
        violations: MutableSequence[m.Tests.Violation],
    ) -> None:
        """Check for missing future annotations import."""
        if u.Tests.approved("MD-003", file_path, approved):
            return
        has_future = c.Tests.VALIDATOR_MD_FUTURE_ANNOTATIONS_MARKER in code
        has_annotations = any(
            ":" in line and not line.strip().startswith("#")
            for line in code.splitlines()
            if "def " in line or "class " in line or "->" in line
        )
        if not has_future and has_annotations:
            violations.append(
                u.Tests.create_violation(
                    file_path,
                    block_start,
                    "MD-003",
                    lines,
                    c.Tests.VALIDATOR_MSG_MD_MISSING_FUTURE,
                )
            )

    @classmethod
    def collect_markdown_files(
        cls,
        project_root: Path,
    ) -> Sequence[Path]:
        """Collect all .md files that may contain Python code blocks."""
        md_files: MutableSequence[Path] = []
        for search_dir in (
            project_root,
            project_root / ".claude" / "skills",
            project_root / "docs",
        ):
            if search_dir.is_dir():
                md_files.extend(search_dir.rglob("*.md"))
        return md_files


__all__: list[str] = ["FlextValidatorMarkdown"]
