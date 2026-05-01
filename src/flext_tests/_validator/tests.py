"""Test validation for FLEXT architecture.

Detects test violations: monkeypatch, mocks, @patch decorator usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
from collections.abc import (
    MutableSequence,
)
from pathlib import Path
from typing import TYPE_CHECKING, override

from flext_tests import FlextTestsValidatorModels, c, t, u

if TYPE_CHECKING:
    from flext_tests import m


class FlextValidatorTests(FlextTestsValidatorModels.Tests.ScannerMixin):
    """Test validation methods for FlextTestsValidator.

    Uses c.Tests.Validator, m.Tests.Validator, u.Tests.Validator.
    """

    _VALIDATOR_KEY = c.Tests.VALIDATOR_TESTS_KEY

    @classmethod
    def _check_mock_usage(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect Mock and MagicMock usage."""
        if u.Tests.approved("TEST-002", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        mock_names = c.Tests.VALIDATOR_APPROVED_MOCK_NAMES
        for node in ast.walk(tree):
            match node:
                case ast.ImportFrom(module=mod, names=names) if (
                    mod and "mock" in mod.lower()
                ):
                    violations.extend(
                        u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "TEST-002",
                            lines,
                            f"import {alias.name}",
                        )
                        for alias in names
                        if alias.name in mock_names
                    )
                case ast.Call(func=ast.Name(id=name)) if name in mock_names:
                    violations.append(
                        u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "TEST-002",
                            lines,
                            f"{name}()",
                        )
                    )
                case _:
                    pass
        return violations

    @classmethod
    def _check_monkeypatch(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect monkeypatch usage in function parameters and calls."""
        if u.Tests.approved("TEST-001", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.args:
                    if arg.arg == "monkeypatch":
                        violation = u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "TEST-001",
                            lines,
                            c.Tests.VALIDATOR_MSG_TEST_MONKEYPATCH.format(
                                func=node.name,
                            ),
                        )
                        violations.append(violation)
            elif (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and (node.value.id == "monkeypatch")
            ):
                violation = u.Tests.create_violation(
                    file_path,
                    node.lineno,
                    "TEST-001",
                    lines,
                    f"monkeypatch.{node.attr}",
                )
                violations.append(violation)
        return violations

    @classmethod
    def _check_patch_decorator(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Detect @patch decorator usage."""
        if u.Tests.approved("TEST-003", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
            ):
                continue
            for decorator in node.decorator_list:
                if cls._is_patch_decorator(decorator):
                    violation = u.Tests.create_violation(
                        file_path,
                        decorator.lineno,
                        "TEST-003",
                        lines,
                    )
                    violations.append(violation)
        return violations

    @classmethod
    def _is_patch_decorator(cls, decorator: ast.expr) -> bool:
        """Check if decorator is @patch or @patch.object, etc."""
        if isinstance(decorator, ast.Name) and decorator.id == "patch":
            return True
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name) and decorator.func.id == "patch":
                return True
            if isinstance(decorator.func, ast.Attribute):
                if (
                    isinstance(decorator.func.value, ast.Name)
                    and decorator.func.value.id == "patch"
                ):
                    return True
                if decorator.func.attr == "patch":
                    return True
        return (
            isinstance(decorator, ast.Attribute)
            and isinstance(decorator.value, ast.Name)
            and (decorator.value.id == "patch")
        )

    @classmethod
    @override
    def _scan_file(
        cls,
        file_path: Path,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Scan a single file for test violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        try:
            content = file_path.read_text(encoding=c.Tests.DEFAULT_ENCODING)
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError, OSError):
            return violations
        lines = content.splitlines()
        violations.extend(cls._check_monkeypatch(file_path, tree, lines, approved))
        violations.extend(cls._check_mock_usage(file_path, tree, lines, approved))
        violations.extend(cls._check_patch_decorator(file_path, tree, lines, approved))
        return violations


__all__: list[str] = ["FlextValidatorTests"]
