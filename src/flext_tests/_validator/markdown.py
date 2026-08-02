"""Markdown code-block validator for flext-tests."""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path

from flext_cli import u
from flext_core import p, t
from flext_tests._constants.validator import FlextTestsConstantsValidator
from flext_tests._models.validator import FlextTestsValidatorModelsMixin
from flext_tests._utilities.validator import FlextTestsValidatorUtilitiesMixin


class FlextValidatorMarkdown:
    """Validate Python code blocks inside markdown docs."""

    @classmethod
    def markdown(
        cls,
        paths: t.SequenceOf[Path],
        *,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[FlextTestsValidatorModelsMixin.ScanResult]:
        """Validate Python code blocks in markdown files."""
        return FlextTestsValidatorUtilitiesMixin.validator_run_scan(
            files=list(paths),
            approved_exceptions=approved_exceptions,
            validator_name=FlextTestsConstantsValidator.VALIDATOR_MARKDOWN_KEY,
            scan_file=cls._scan_file,
        )

    @classmethod
    def _scan_file(
        cls, file_path: Path, approved: t.MappingKV[str, t.StrSequence]
    ) -> t.SequenceOf[FlextTestsValidatorModelsMixin.Violation]:
        """Scan a single markdown file for Python code block violations."""
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation] = []
        read = u.Cli.files_read_text(file_path)
        if read.failure:
            return [
                FlextTestsValidatorUtilitiesMixin.create_violation(
                    file_path,
                    0,
                    "MD-UNREADABLE",
                    (),
                    read.error or "could not read file",
                )
            ]
        content = read.value
        lines = content.splitlines()
        for match in FlextTestsConstantsValidator.VALIDATOR_MD_PYTHON_BLOCK_RE.finditer(
            content
        ):
            info = match.group("info")
            code = match.group("code")
            block_start = content[: match.start()].count("\n") + 1
            is_notest = FlextTestsConstantsValidator.VALIDATOR_MD_NOTEST_MARKER in info
            if not is_notest:
                cls._check_syntax(file_path, code, lines, block_start, violations)
            cls._check_forbidden_imports(
                file_path, code, lines, block_start, approved, violations
            )
            cls._check_object_annotations(
                file_path, code, lines, block_start, approved, violations
            )
            cls._check_any_annotations(
                file_path, code, lines, block_start, approved, violations
            )
            cls._check_future_annotations(
                file_path, code, lines, block_start, approved, violations
            )
        return violations

    @classmethod
    def _check_syntax(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation],
    ) -> None:
        """Check that a Python code block is syntactically valid."""
        try:
            compile(code, str(file_path), "exec")
        except SyntaxError:
            violations.append(
                FlextTestsValidatorUtilitiesMixin.create_violation(
                    file_path,
                    block_start,
                    "MD-001",
                    lines,
                    FlextTestsConstantsValidator.VALIDATOR_MSG_MD_SYNTAX.format(
                        msg="invalid Python"
                    ),
                )
            )

    @classmethod
    def _check_forbidden_imports(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        approved: t.MappingKV[str, t.StrSequence],
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation],
    ) -> None:
        """Check for forbidden typing imports via line scanning."""
        if FlextTestsValidatorUtilitiesMixin.approved("MD-002", file_path, approved):
            return
        for line_offset, code_line in enumerate(code.splitlines()):
            stripped = code_line.strip()
            if not stripped.startswith(
                FlextTestsConstantsValidator.VALIDATOR_MD_TYPING_IMPORT_PREFIX
            ):
                continue
            for (
                name
            ) in FlextTestsConstantsValidator.VALIDATOR_MD_FORBIDDEN_TYPING_NAMES:
                if name in stripped:
                    violations.append(
                        FlextTestsValidatorUtilitiesMixin.create_violation(
                            file_path,
                            block_start + line_offset + 1,
                            "MD-002",
                            lines,
                            FlextTestsConstantsValidator.VALIDATOR_MSG_MD_FORBIDDEN_IMPORT.format(
                                import_name=f"from typing import {name}"
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
        approved: t.MappingKV[str, t.StrSequence],
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation],
    ) -> None:
        """Check for 'object' used as type annotation."""
        if FlextTestsValidatorUtilitiesMixin.approved("MD-004", file_path, approved):
            return
        for line_offset, code_line in enumerate(code.splitlines()):
            if FlextTestsConstantsValidator.VALIDATOR_MD_OBJECT_ANNOTATION_RE.search(
                code_line
            ):
                violations.append(
                    FlextTestsValidatorUtilitiesMixin.create_violation(
                        file_path,
                        block_start + line_offset + 1,
                        "MD-004",
                        lines,
                        FlextTestsConstantsValidator.VALIDATOR_MSG_MD_FORBIDDEN_ANNOTATION.format(
                            annotation="object"
                        ),
                    )
                )

    @classmethod
    def _check_any_annotations(
        cls,
        file_path: Path,
        code: str,
        lines: t.StrSequence,
        block_start: int,
        approved: t.MappingKV[str, t.StrSequence],
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation],
    ) -> None:
        """Check for 'Any' used as type annotation."""
        if FlextTestsValidatorUtilitiesMixin.approved("MD-005", file_path, approved):
            return
        for line_offset, code_line in enumerate(code.splitlines()):
            if FlextTestsConstantsValidator.VALIDATOR_MD_ANY_ANNOTATION_RE.search(
                code_line
            ):
                violations.append(
                    FlextTestsValidatorUtilitiesMixin.create_violation(
                        file_path,
                        block_start + line_offset + 1,
                        "MD-005",
                        lines,
                        FlextTestsConstantsValidator.VALIDATOR_MSG_MD_FORBIDDEN_ANNOTATION.format(
                            annotation="Any"
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
        approved: t.MappingKV[str, t.StrSequence],
        violations: MutableSequence[FlextTestsValidatorModelsMixin.Violation],
    ) -> None:
        """Check for missing future annotations import."""
        if FlextTestsValidatorUtilitiesMixin.approved("MD-003", file_path, approved):
            return
        has_future = (
            FlextTestsConstantsValidator.VALIDATOR_MD_FUTURE_ANNOTATIONS_MARKER in code
        )
        has_annotations = any(
            ":" in line and not line.strip().startswith("#")
            for line in code.splitlines()
            if "def " in line or "class " in line or "->" in line
        )
        if not has_future and has_annotations:
            violations.append(
                FlextTestsValidatorUtilitiesMixin.create_violation(
                    file_path,
                    block_start,
                    "MD-003",
                    lines,
                    FlextTestsConstantsValidator.VALIDATOR_MSG_MD_MISSING_FUTURE,
                )
            )


__all__: list[str] = ["FlextValidatorMarkdown"]
