"""Type validation for FLEXT architecture.

Detects type violations: type suppression comments, wildcard types, unapproved usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import re
from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import TYPE_CHECKING, override

from flext_tests import FlextTestsValidatorModels, c, t, u

if TYPE_CHECKING:
    from flext_tests import m


class FlextValidatorTypes(FlextTestsValidatorModels.Tests.ScannerMixin):
    """Type validation methods for FlextTestsValidator.

    Uses c.Tests.Validator, m.Tests.Validator, u.Tests.Validator.
    """

    _VALIDATOR_KEY = c.Tests.VALIDATOR_TYPES_KEY

    @staticmethod
    def _annotation_names(node: ast.AST, names: frozenset[str]) -> set[str]:
        """Return matching typing symbols referenced anywhere inside one annotation."""
        matches: set[str] = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id in names:
                matches.add(child.id)
            elif isinstance(child, ast.Attribute) and child.attr in names:
                matches.add(child.attr)
            elif isinstance(child, ast.Constant) and child.value in names:
                matches.add(str(child.value))
        return matches

    @classmethod
    def _check_legacy_typing_factories(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect pre-PEP 695 typing factories and Generic base syntax."""
        if u.Tests.approved("TYPE-004", file_path, approved):
            return []

        def _emit(line: int, name: str) -> m.Tests.Violation:
            return u.Tests.create_violation(
                file_path,
                line,
                "TYPE-004",
                lines,
                c.Tests.VALIDATOR_MSG_TYPE_LEGACY_FACTORY.format(name=name),
            )

        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            match node:
                case ast.Call(func=func):
                    violations.extend(
                        _emit(node.lineno, name)
                        for name in sorted(
                            cls._annotation_names(
                                func, c.Tests.VALIDATOR_LEGACY_FACTORY_NAMES
                            )
                        )
                    )
                case ast.AnnAssign(annotation=ann):
                    violations.extend(
                        _emit(node.lineno, name)
                        for name in sorted(
                            cls._annotation_names(ann, frozenset({"TypeAlias"}))
                        )
                    )
                case ast.ClassDef(bases=bases):
                    for base in bases:
                        violations.extend(
                            _emit(getattr(base, "lineno", node.lineno), name)
                            for name in sorted(
                                cls._annotation_names(
                                    base, c.Tests.VALIDATOR_LEGACY_BASE_NAMES
                                )
                            )
                        )
        return violations

    @classmethod
    def _check_legacy_typing_annotations(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect legacy annotation constructs superseded by modern Python 3.13 syntax."""
        if u.Tests.approved("TYPE-005", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        annotations: MutableSequence[tuple[int, ast.AST]] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns is not None:
                    annotations.append((node.lineno, node.returns))
                for arg in (
                    *node.args.args,
                    *node.args.kwonlyargs,
                    node.args.vararg,
                    node.args.kwarg,
                ):
                    if arg is not None and arg.annotation is not None:
                        annotations.append(
                            (getattr(arg, "lineno", node.lineno), arg.annotation),
                        )
            elif isinstance(node, ast.AnnAssign):
                annotations.append((node.lineno, node.annotation))
        for line_number, annotation in annotations:
            matches = cls._annotation_names(
                annotation,
                c.Tests.VALIDATOR_LEGACY_ANNOTATION_NAMES,
            )
            for match in sorted(matches):
                violations.append(
                    u.Tests.create_violation(
                        file_path,
                        line_number,
                        "TYPE-005",
                        lines,
                        c.Tests.VALIDATOR_MSG_TYPE_LEGACY_ANNOTATION.format(
                            name=match,
                        ),
                    ),
                )
        return violations

    @classmethod
    def _check_object_annotations(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect forbidden `object` annotations in governed code."""
        if u.Tests.approved("TYPE-006", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns is not None and cls._annotation_names(
                    node.returns,
                    frozenset({"object"}),
                ):
                    violations.append(
                        u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "TYPE-006",
                            lines,
                            c.Tests.VALIDATOR_MSG_TYPE_OBJECT_ANNOTATION.format(
                                location=f"return type of '{node.name}'",
                            ),
                        ),
                    )
                for arg in (*node.args.args, *node.args.kwonlyargs):
                    if arg.annotation is None or not cls._annotation_names(
                        arg.annotation,
                        frozenset({"object"}),
                    ):
                        continue
                    violations.append(
                        u.Tests.create_violation(
                            file_path,
                            getattr(arg, "lineno", node.lineno),
                            "TYPE-006",
                            lines,
                            c.Tests.VALIDATOR_MSG_TYPE_OBJECT_ANNOTATION.format(
                                location=f"argument '{arg.arg}'",
                            ),
                        ),
                    )
            elif isinstance(node, ast.AnnAssign):
                if not cls._annotation_names(node.annotation, frozenset({"object"})):
                    continue
                violations.append(
                    u.Tests.create_violation(
                        file_path,
                        node.lineno,
                        "TYPE-006",
                        lines,
                        c.Tests.VALIDATOR_MSG_TYPE_OBJECT_ANNOTATION.format(
                            location="variable annotation",
                        ),
                    ),
                )
        return violations

    @classmethod
    def _check_bool_returning_is_helpers(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect `is_*` helpers still returning bool instead of TypeIs or a renamed predicate."""
        if u.Tests.approved("TYPE-007", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("is_") or node.returns is None:
                continue
            if not cls._annotation_names(node.returns, frozenset({"bool"})):
                continue
            violations.append(
                u.Tests.create_violation(
                    file_path,
                    node.lineno,
                    "TYPE-007",
                    lines,
                    c.Tests.VALIDATOR_MSG_TYPE_BOOL_IS_HELPER.format(name=node.name),
                ),
            )
        return violations

    @classmethod
    def _check_any_types(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect wildcard type annotations."""
        if u.Tests.approved("TYPE-002", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns and u.Tests.any_type(node.returns):
                    violation = u.Tests.create_violation(
                        file_path,
                        node.lineno,
                        "TYPE-002",
                        lines,
                        c.Tests.VALIDATOR_MSG_TYPE_ANY_RETURN,
                    )
                    violations.append(violation)
                for arg in node.args.args + node.args.kwonlyargs:
                    if arg.annotation and u.Tests.any_type(arg.annotation):
                        violation = u.Tests.create_violation(
                            file_path,
                            arg.lineno if hasattr(arg, "lineno") else node.lineno,
                            "TYPE-002",
                            lines,
                            c.Tests.VALIDATOR_MSG_TYPE_ANY_ARG.format(arg=arg.arg),
                        )
                        violations.append(violation)
            elif isinstance(node, ast.AnnAssign):
                if node.annotation and u.Tests.any_type(node.annotation):
                    violation = u.Tests.create_violation(
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
            c.Tests.VALIDATOR_APPROVED_CAST_PATTERNS,
        )
        file_str = str(file_path)
        if any(re.search(pattern, file_str) for pattern in patterns):
            return []
        return [
            u.Tests.create_violation(
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
        if u.Tests.approved("TYPE-001", file_path, approved):
            return []
        pattern = re.compile(r"#\s*type:\s*ignore")
        return [
            u.Tests.create_violation(
                file_path,
                i,
                "TYPE-001",
                lines,
            )
            for i, line in enumerate(lines, start=1)
            if pattern.search(line) and u.Tests.real_comment(line, pattern)
        ]

    @classmethod
    @override
    def _scan_file(
        cls,
        file_path: Path,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Scan a single file for type violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        try:
            content = file_path.read_text(encoding=c.Tests.DEFAULT_ENCODING)
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
        violations.extend(
            cls._check_legacy_typing_factories(file_path, tree, lines, approved),
        )
        violations.extend(
            cls._check_legacy_typing_annotations(file_path, tree, lines, approved),
        )
        violations.extend(
            cls._check_object_annotations(file_path, tree, lines, approved)
        )
        violations.extend(
            cls._check_bool_returning_is_helpers(file_path, tree, lines, approved),
        )
        return violations


__all__: list[str] = ["FlextValidatorTypes"]
