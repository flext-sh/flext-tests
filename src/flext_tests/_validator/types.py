"""Type validation for FLEXT architecture.

Detects type violations: type suppression comments, wildcard types, unapproved usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from collections.abc import Mapping, MutableSequence, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import r
from flext_tests import c, t, u, vm

if TYPE_CHECKING:
    from flext_tests import m


class FlextValidatorTypes:
    """Type validation methods for FlextTestsValidator.

    Uses c.Tests.Validator, m.Tests.Validator, u.Tests.Validator.
    """

    @classmethod
    def _check_any_types(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect wildcard type annotations."""
        if u.Tests.Validator.is_approved("TYPE-002", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns and u.Tests.Validator.is_any_type(node.returns):
                    violation = u.Tests.Validator.create_violation(
                        file_path,
                        node.lineno,
                        "TYPE-002",
                        lines,
                        c.Tests.Validator.Messages.TYPE_ANY_RETURN,
                    )
                    violations.append(violation)
                for arg in node.args.args + node.args.kwonlyargs:
                    if arg.annotation and u.Tests.Validator.is_any_type(arg.annotation):
                        violation = u.Tests.Validator.create_violation(
                            file_path,
                            arg.lineno if hasattr(arg, "lineno") else node.lineno,
                            "TYPE-002",
                            lines,
                            c.Tests.Validator.Messages.TYPE_ANY_ARG.format(arg=arg.arg),
                        )
                        violations.append(violation)
            elif isinstance(node, ast.AnnAssign):
                if node.annotation and u.Tests.Validator.is_any_type(node.annotation):
                    violation = u.Tests.Validator.create_violation(
                        file_path,
                        node.lineno,
                        "TYPE-002",
                        lines,
                        "in variable annotation",
                    )
                    violations.append(violation)
        return violations

    @classmethod
    def _check_cast_usage(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect unapproved  usage."""
        patterns = list(approved.get("TYPE-003", [])) + list(
            c.Tests.Validator.Approved.CAST_PATTERNS,
        )
        file_str = str(file_path)
        if any(re.search(pattern, file_str) for pattern in patterns):
            return []
        return [
            u.Tests.Validator.create_violation(
                file_path,
                node.lineno,
                "TYPE-003",
                lines,
            )
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and (
                (isinstance(node.func, ast.Name) and node.func.id == "cast")
                or (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "cast"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "typing"
                )
            )
        ]

    @classmethod
    def _check_type_ignore(
        cls,
        file_path: Path,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect type: ignore comments in code (not in strings/docstrings)."""
        if u.Tests.Validator.is_approved("TYPE-001", file_path, approved):
            return []
        pattern = re.compile(r"#\s*type:\s*ignore")
        return [
            u.Tests.Validator.create_violation(
                file_path,
                i,
                "TYPE-001",
                lines,
            )
            for i, line in enumerate(lines, start=1)
            if pattern.search(line) and u.Tests.Validator.is_real_comment(line, pattern)
        ]

    @classmethod
    def _scan_file(
        cls,
        file_path: Path,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Scan a single file for type violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return violations
        lines = content.splitlines()
        violations.extend(cls._check_type_ignore(file_path, lines, approved))
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            return violations
        violations.extend(cls._check_any_types(file_path, tree, lines, approved))
        violations.extend(cls._check_cast_usage(file_path, tree, lines, approved))
        return violations

    @classmethod
    def scan(
        cls,
        files: Sequence[Path],
        approved_exceptions: Mapping[str, t.StrSequence] | None = None,
    ) -> r[m.Tests.ScanResult]:
        """Scan files for type violations.

        Args:
            files: List of Python files to scan
            approved_exceptions: Dict mapping rule IDs to list of approved file patterns

        Returns:
            r with ScanResult containing all violations found

        """
        return vm.ScanCommon.run_scan(
            files=files,
            approved_exceptions=approved_exceptions,
            validator_name=c.Tests.Validator.Defaults.VALIDATOR_TYPES,
            scan_file=cls._scan_file,
        )


__all__ = ["FlextValidatorTypes"]
