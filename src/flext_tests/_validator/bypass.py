"""Bypass validation for FLEXT architecture.

Detects bypass patterns: noqa comments, pragma: no cover, exception swallowing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import re
from collections.abc import (
    MutableSequence,
)
from pathlib import Path
from typing import override

from flext_tests import FlextTestsValidatorModels, c, m, t, u


class FlextValidatorBypass(FlextTestsValidatorModels.Tests.ScannerMixin):
    """Bypass validation methods for FlextTestsValidator.

    Uses c.Tests.Validator for constants and m.Tests.Validator for models.
    """

    _VALIDATOR_KEY = c.Tests.VALIDATOR_BYPASS_KEY

    @classmethod
    def _check_exception_swallowing(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect exception swallowing patterns (bare except or except with pass)."""
        if u.Tests.approved("BYPASS-003", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    violation = u.Tests.create_violation(
                        file_path,
                        node.lineno,
                        "BYPASS-003",
                        lines,
                        c.Tests.VALIDATOR_MSG_BYPASS_BARE_EXCEPT,
                    )
                    violations.append(violation)
                elif u.Tests.only_pass(node.body):
                    violation = u.Tests.create_violation(
                        file_path,
                        node.lineno,
                        "BYPASS-003",
                        lines,
                        c.Tests.VALIDATOR_MSG_BYPASS_ONLY_PASS,
                    )
                    violations.append(violation)
        return violations

    @classmethod
    def _check_noqa(
        cls,
        file_path: Path,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect # noqa comments."""
        if u.Tests.approved("BYPASS-001", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        pattern = re.compile(r"#\s*noqa", re.IGNORECASE)
        for i, line in enumerate(lines, start=1):
            is_real = u.Tests.real_comment(line, pattern)
            if pattern.search(line) and is_real:
                violation = u.Tests.create_violation(
                    file_path,
                    i,
                    "BYPASS-001",
                    lines,
                )
                violations.append(violation)
        return violations

    @classmethod
    def _check_pragma_no_cover(
        cls,
        file_path: Path,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect # pragma: no cover comments."""
        patterns = list(approved.get("BYPASS-002", [])) + list(
            c.Tests.VALIDATOR_APPROVED_PRAGMA_PATTERNS,
        )
        file_str = str(file_path)
        if any(re.search(pattern, file_str) for pattern in patterns):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        pattern = re.compile(r"#\s*pragma:\s*no\s*cover", re.IGNORECASE)
        for i, line in enumerate(lines, start=1):
            is_real = u.Tests.real_comment(line, pattern)
            if pattern.search(line) and is_real:
                violation = u.Tests.create_violation(
                    file_path,
                    i,
                    "BYPASS-002",
                    lines,
                )
                violations.append(violation)
        return violations

    @override
    @classmethod
    def _scan_file(
        cls,
        file_path: Path,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Scan a single file for bypass violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        try:
            content = file_path.read_text(encoding=c.Tests.DEFAULT_ENCODING)
        except (OSError, UnicodeDecodeError):
            return violations
        lines = content.splitlines()
        violations.extend(cls._check_noqa(file_path, lines, approved))
        violations.extend(cls._check_pragma_no_cover(file_path, lines, approved))
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            return violations
        violations.extend(
            cls._check_exception_swallowing(file_path, tree, lines, approved),
        )
        return violations


__all__: list[str] = ["FlextValidatorBypass"]
